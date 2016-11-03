<?php
header("Content-Type:application/json;charset=utf-8");

$imgs = isset($_POST['imgs']) ? $_POST['imgs'] : [];

if (count($imgs) == 0) {
    http_response_code(400);
    echo json_encode(['msg' => '缺少上传图片数据']);
    exit;
}

$uploadPath = './upload/';
foreach ($imgs as $img) {
    $img = str_replace('data:image/jpeg;base64,', '', $img);
    $file = $uploadPath . time() . mt_rand(100, 999) . '.jpeg';
    file_put_contents($file, base64_decode($img));
}

echo json_encode(['msg' => '上传成功', 'file' => $file]);