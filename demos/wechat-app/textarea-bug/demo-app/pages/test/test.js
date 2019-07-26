Page({
  data: {
    inputContent: ''
  },
  clearInputContent(e) {
    const mode = parseInt(e.target.dataset.mode)

    switch (mode) {
      case 1:
        this.setData({
          inputContent: ''
        })
        break;
      case 2:
        this.setData({
          inputContent: ' '
        })
        this.setData({
          inputContent: ''
        })
        break;
      case 3:
        this.setData({
          inputContent: ' '
        })
        setTimeout(_ => {
          this.setData({
            inputContent: ''
          })
        }, 300)
        break;
    }
  }
})