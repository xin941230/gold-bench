#!/usr/bin/env node
/**
 * cors-proxy.js — 本地 CORS 代理（黄金交易工作台 v2.15 配套）
 *
 * 解决的问题：GitHub Pages 上的工作台直接用浏览器请求上游接口
 *   （如 https://open.bigmodel.cn 智谱 BigModel、https://api.deepseek.com）
 *   时，大概率被浏览器跨域策略(CORS)拦截，导致「联网 AI」偶发失败。
 * 这个代理在本机起一个 HTTP 服务，工作台改为请求 http://localhost:PORT，
 *   由它转发到上游并把响应（含流式 SSE）原样回传，从而彻底绕开跨域。
 *
 * 用法（在 site 目录下，用本机 Node 运行）：
 *   node cors-proxy.js            # 默认端口 3000
 *   PORT=8080 node cors-proxy.js  # 自定义端口
 *
 * 然后在工作台 ⚙️ 设置里：勾选「本地代理」，代理地址填 http://localhost:3000 并保存。
 *
 * 说明：
 *   - 代理只转发请求，不保存你的 Key（Key 由浏览器随请求头带来，原样转给上游）。
 *   - 已加上 Chrome「私有网络访问(Private Network Access)」所需的响应头，
 *     确保从 HTTPS 页面访问 localhost 不被拦。
 *   - 仅监听 127.0.0.1，外网无法访问，相对安全。
 */

'use strict';

const http = require('http');
const https = require('https');
const { URL } = require('url');

const PORT = parseInt(process.env.PORT || '3000', 10);
const UPSTREAM = 'https://open.bigmodel.cn/api/paas/v4/'; // 智谱 BigModel OpenAI 兼容接口（默认上游，尾部斜杠是路径拼接关键）
const ALLOW_HOSTS = ['open.bigmodel.cn', 'api.deepseek.com']; // 仅允许转发到这些上游，避免成开放代理

// 统一 CORS + 私有网络访问响应头
const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS,PATCH',
  'Access-Control-Allow-Headers': 'Content-Type,Authorization,Accept',
  'Access-Control-Max-Age': '86400',
  'Access-Control-Allow-Private-Network': 'true'
};

function sendText(res, code, text, extra) {
  const headers = Object.assign({ 'Content-Type': 'text/plain; charset=utf-8' }, CORS_HEADERS, extra || {});
  res.writeHead(code, headers);
  res.end(text);
}

const server = http.createServer(function (req, res) {
  // 预检请求：直接放行（含私有网络访问预检）
  if (req.method === 'OPTIONS') {
    sendText(res, 204, '');
    return;
  }

  let target;
  try {
    // 注意：req.url 以 '/' 开头时 new URL(req.url, base) 会当成根相对路径、丢掉 base 的目录，
    // 必须显式拼到 base 目录下，否则智谱会变成 open.bigmodel.cn/chat/completions（错误路径→405）
    const base = new URL(UPSTREAM);
    base.pathname = base.pathname.replace(/\/+$/, '') + '/' + req.url.replace(/^\/+/, '');
    base.search = '';
    target = base;
  } catch (e) {
    sendText(res, 400, 'Bad request url: ' + req.url);
    return;
  }

  // 只允许转发到白名单上游，避免被当成开放代理
  if (!ALLOW_HOSTS.includes(target.hostname)) {
    sendText(res, 403, '只允许代理到 ' + ALLOW_HOSTS.join(' / '));
    return;
  }

    // 读取请求体（AI 请求体很小，无需流式上传），再原样转发，避免管道方式偶发的 405
    const chunks = [];
    req.on('data', function (c) { chunks.push(c); });
    req.on('end', function () {
      const body = Buffer.concat(chunks);
      // 只转发核心请求头，丢弃 accept-encoding / sec-fetch-* / accept-language 等
      // 可能触发上游 WAF（nginx 405）的浏览器衍生头
      const fwd = {
        method: req.method,
        hostname: target.hostname,
        port: target.port || 443,
        path: target.pathname + target.search,
        headers: { host: target.hostname }
      };
      ['content-type', 'authorization', 'user-agent', 'origin', 'accept', 'referer'].forEach(function (k) {
        if (req.headers[k]) fwd.headers[k] = req.headers[k];
      });
      if (body.length) fwd.headers['Content-Length'] = String(body.length);

    const upstreamReq = https.request(fwd, function (upstreamRes) {
      const outHeaders = Object.assign({}, upstreamRes.headers, CORS_HEADERS);
      res.writeHead(upstreamRes.statusCode, outHeaders);
      upstreamRes.pipe(res);
    });

    upstreamReq.on('error', function (err) {
      sendText(res, 502, 'Proxy upstream error: ' + err.message);
    });

    if (body.length) upstreamReq.write(body);
    upstreamReq.end();
  });
});

server.listen(PORT, '127.0.0.1', function () {
  console.log('✅ CORS 代理已启动： http://localhost:' + PORT);
  console.log('   默认上游： ' + UPSTREAM + '（白名单：' + ALLOW_HOSTS.join(' / ') + '）');
  console.log('   在工作台 ⚙️ 设置里勾选「本地代理」，地址填 http://localhost:' + PORT + ' 并保存。');
  console.log('   按 Ctrl+C 停止。');
});

server.on('error', function (err) {
  console.error('❌ 代理启动失败：', err.message);
  process.exit(1);
});
