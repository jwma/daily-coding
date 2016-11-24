const constant = require('./utils/constant.js')
const apiURL = require('./utils/api-url.js')

App({
  onLaunch: function () {

  },
  appStartUp(cb) {
    if (!wx.getStorageSync(constant.TMP_FILE_FOR_POST)) {

      wx.downloadFile({
        url: 'https://wa1.majiawei.com/files/1.png', //仅为示例，并非真实的资源
        success: function (res) {

          wx.saveFile({
            tempFilePath: res.tempFilePath,
            success(res) {
              wx.setStorage({
                key: constant.TMP_FILE_FOR_POST,
                data: res.savedFilePath,
                success() {
                  typeof cb == "function" && cb()
                }
              })
            }
          })

        }
      })
    }

  },
  getPostList(page, cb) {
    wx.request({
      url: apiURL.POST_LIST + '?page=' + page,
      data: {},
      method: 'GET',
      success(res) {
        typeof cb == "function" && cb(res.data)
      }
    })
  },
  getPostDetails(id, cb, failCb) {
    wx.request({
      url: apiURL.POST_DETAIL + id,
      method: 'GET',
      success(res) {
        if (res.statusCode != 200) {
          typeof failCb == "function" && failCb()
        } else {
          typeof cb == "function" && cb(res.data)
        }
      }
    })
  },
  getCommentList(postId, page, cb) {
    wx.request({
      url: apiURL.COMMENT_LIST + '?postId=' + postId + '&page=' + page,
      method: 'GET',
      success: function (res) {
        typeof cb == "function" && cb(res.data)
      }
    })
  },
  replyPost(replyData, cb, failCb) {

  },
  userInfo: null,
  session: {
    code: null,
    createdAt: null
  }
})