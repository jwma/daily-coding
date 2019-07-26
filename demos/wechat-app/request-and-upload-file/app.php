<?php
function getParameter($name, $default = null) {
    return isset($_REQUEST[$name]) ? $_REQUEST[$name] : $default;
}

function jsonResponse(array $content = [], $code = 200) {
    http_response_code($code);
    header('Content-Type: application/json');
    echo json_encode($content);
    exit;
}

function isMethod($method) {
    return $_SERVER['REQUEST_METHOD'] === strtoupper($method);
}

function index() {
    echo 'welcome';
    return;
}

function wxRequest() {
    $code = getParameter('code');

    return jsonResponse(['action' => 'wxRequest', 'msg' => 'ok', 'codeInRequest' => $code], $code);
}

function wxUploadFile() {
    if (!isMethod('post')) {
        return jsonResponse(['action' => 'wxUploadFile', 'msg' => 'method not allowed'], 405);
    }

    $code = getParameter('code');

    return jsonResponse(['action' => 'wxUploadFile','msg' => 'ok', 'codeInRequest' => $code], $code);
}

$action = getParameter('action', 'index');
$action();