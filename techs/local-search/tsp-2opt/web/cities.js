/**
 * 显示小店
 * @class
 * @param map{AMap.Map}
 * @constructor
 */
S.Leads = function (map) {
    this.map = map;
    this.layer = new Loca.RoundPointLayer({
        map: map,
        fitView: true,
    });
};

/**
 * @private
 */
S.Leads.prototype.m_initStyle = function () {

    this.layer.setOptions({
        style: {
            // 默认半径单位为像素
            radius: 6,
            color: '#E8641C',
            borderColor: '#E8641C',
            opacity: 0.75
        }
    });
};

S.Leads.prototype.loadData = function (data) {
    this.layer.setData(data, {
            lnglat: 'coordinates',  // 小店的位置
        });
};

S.Leads.prototype.render = function () {
    this.m_initStyle();
    this.layer.render();
};
