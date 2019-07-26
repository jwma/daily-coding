<?php
header("Content-Type:application/json;charset=utf-8");

$imgs = isset($_POST['imgs']) ? $_POST['imgs'] : [];

// 如果上传的图片数据为空
if (count($imgs) == 0) {
    http_response_code(400);
    echo json_encode(['msg' => '缺少上传图片数据']);
    exit;
}

// 将文件保存到 upload 目录并取一个相对随机的名字
$uploadPath = './upload/';
foreach ($imgs as $img) {
    // 获取图片文件需要的部分数据，然后写入到文件
    $img = str_replace('data:image/jpeg;base64,', '', $img);
    $file = $uploadPath . time() . mt_rand(100, 999) . '.jpeg';
    file_put_contents($file, base64_decode($img));
}

echo json_encode(['msg' => '上传成功', 'file' => $file]);