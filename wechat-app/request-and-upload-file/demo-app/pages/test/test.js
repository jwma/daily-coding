Page({
  data: {
    output: ''
  },
  doWxRequest(e) {
    const self = this
    const code = e.target.dataset.code

    wx.request({
      url: 'http://localhost:8080/api/test-wx-request/' + code,
      data: {},
      method: 'GET',
      success(res) {
        console.log(res, 'success')

        let output = `[wx.request] 进入 success 回调, status code 为 ${res.statusCode}`

        self.setData({
          output: output
        })
      },
      fail(res) {
        console.log(res, 'fail')

        let output = `[wx.request] 进入 fail 回调, status code 为 ${res.statusCode}`

        self.setData({
          output: output
        })

      }
    })
  },
  doWxUploadFile(e) {
    const self = this
    const code = e.target.dataset.code

    wx.uploadFile({
      url: 'http://localhost:8080/api/test-wx-upload-file/' + code,
      filePath: 'wxfile://store_276701038o6zAJs-zJZU51bfk9deknjxUrxFM1479958339356.png', // 我预先保存了一个文件在小程序内
      name: 'name',
      success(res) {
        console.log(res, 'success')

        let output = `[wx.uploadFile] 进入 success 回调, status code 为 ${res.statusCode}`

        self.setData({
          output: output
        })

      },
      fail(res) {
        console.log(res, 'fail')

        let output = `[wx.uploadFile] 进入 fail 回调, ${res.errMsg}`

        self.setData({
          output: output
        })

      }
    })

  }
})