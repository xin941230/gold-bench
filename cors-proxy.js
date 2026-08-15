#!/usr/bin/env node
/**
 * cors-proxy.js — 本地 CORS 代理（黄金交易工作台 v2.14 配套）
 *
 * 解决的问题：GitHub Pages 上的工作台直接用浏览器请求 https://api.deepseek.com
 *   时，大概率被浏览器跨域策略(CORS)拦截，导致「联网 DeepSeek」偶发失败。
 * 这个代理在本机起一个 HTTP 服务，工作台改为请求 http://localhost:PORT，
 *   由它转发到 DeepSeek 并把响应（含流式 SSE）原样回传，从而彻底绕开跨域。
 *
 * 用法（在 site 目录下，用本机 Node 运行）：
 *   node cors-proxy.js            # 默认端口 3000
 *   PORT=8080 node cors-proxy.js  # 自定义端口
 *
 * 然后在工作台 ⚙️ 设置里：勾选「本地代理」，代理地址填 http://localhost:3000 并保存。
 *
 * 说明：
 *   - 代理只转发请求，不保存你的 Key（Key 由浏览器随请求头带来，原样转给 DeepSeek）。
 *   - 已加上 Chrome「私有网络访问(Private Network Access)」所需的响应头，
 *     确保从 HTTPS 页面访问 localhost 不被拦。
 *   - 仅监听 127.0.0.1，外网无法访问，相对安全。
 */

'use strict';

const http = require('http');
const https = require('https');
const { URL } = require('url');

const PORT = parseInt(process.env.PORT || '3000', 10);
const UPSTREAM = 'https://api.deepseek.com'; // DeepSeek OpenAI 兼容接口

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
    target = new URL(req.url, UPSTREAM);
  } catch (e) {
    sendText(res, 400, 'Bad request url: ' + req.url);
    return;
  }

  // 只允许转发到 DeepSeek 上游，避免被当成开放代理
  if (target.hostname !== 'api.deepseek.com') {
    sendText(res, 403, '只允许代理到 api.deepseek.com');
    return;
  }

  const options = {
    method: req.method,
    hostname: target.hostname,
    port: target.port || 443,
    path: target.pathname + target.search,
    headers: Object.assign({}, req.headers, { host: target.hostname })
  };
  // 去掉可能带来问题的逐跳头
  delete options.headers['connection'];

  const upstreamReq = https.request(options, function (upstreamRes) {
    const outHeaders = Object.assign({}, upstreamRes.headers, CORS_HEADERS);
    // 透传上游状态码与（可能 gzip 的）响应体
    res.writeHead(upstreamRes.statusCode, outHeaders);
    upstreamRes.pipe(res);
  });

  upstreamReq.on('error', function (err) {
    sendText(res, 502, 'Proxy upstream error: ' + err.message);
  });

  req.pipe(upstreamReq);
});

server.listen(PORT, '127.0.0.1', function () {
  console.log('✅ DeepSeek CORS 代理已启动： http://localhost:' + PORT);
  console.log('   上游目标： ' + UPSTREAM);
  console.log('   在工作台 ⚙️ 设置里勾选「本地代理」，地址填 http://localhost:' + PORT + ' 并保存。');
  console.log('   按 Ctrl+C 停止。');
});

server.on('error', function (err) {
  console.error('❌ 代理启动失败：', err.message);
  process.exit(1);
});
