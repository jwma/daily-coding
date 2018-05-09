/**
 * 计算x日起到n天后的（包含x日） "x月x日 周x" 格式列表
 * 参数：
 *    startTimestamp: 起始日期时间戳
 *    days: 计算到多少天后
 *    formatFunc: 格式化结果数据
 * 返回：
 * {
 *   month: 月, 1,2,3,4,5,6,7,8,9,10,11,12
 *   date: 日，最小1，最大31
 *   day: 当日是周几，0,1,2,3,4,5,6，0为周日
 * }
 */
function generateDates(startTimestamp, days, formatFunc) {
    days = days || 0
    const result = []
    const oneDay = 86400000

    for (let i = 0; i < days + 1; i++) {
        let dateHelper = new Date(startTimestamp + (i * oneDay))
        let year = dateHelper.getFullYear()
        let month = monthText = dateHelper.getMonth() + 1
        let date = dateText = dateHelper.getDate()
        let day = dayText = dateHelper.getDay()
        result.push({year, month, monthText, date, dateText, day, dayText})
    }
    return typeof formatFunc === 'function' ? formatFunc(result) : result
}

/**
 * 获取今日0点0时0分0秒时间戳
 */
function getTodayTimestamp() {
    const today = new Date()
    today.setHours(0)
    today.setMinutes(0)
    today.setSeconds(0)
    today.setMilliseconds(0)
    return today.getTime()
}

generateDates(getTodayTimestamp(), 3, dates => {
    let dayMapping = {0: '日', 1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六'}
    const result = []
    dates.forEach((one) => {
        let {month, date, day} = one
        let monthText = month < 10 ? `0${month}月` : `${month}月`
        let dateText = date < 10 ? `0${date}日` : `${date}日`
        let dayText = `周${dayMapping[day]}`
        result.push(Object.assign(one, {monthText, dateText, dayText}))
    })
    return result
})