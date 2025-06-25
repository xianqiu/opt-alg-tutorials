/**
 * 显示砖块(填充的多边形)
 * @class
 * @param{AMap.Map} map
 * @constructor
 */
MS.Bricks = function (map) {
    this.map = map;
    this.layer = new Loca.PolygonLayer({
        map: map,
        fitView: true
    });
};

/**
 * 设置显示的样式
 * @private
 */
MS.Bricks.prototype.m_initStyle = function() {

    this.layer.setOptions({
        style: {
            opacity: 0.3,
            color: '#a1dab4',
            borderWidth: 2,
            borderColor: '#ff5123'
        },
        // 鼠标选中
        selectStyle: {
            radius: 14,
            color: '#FFF684',
        }
    });
};


MS.Bricks.prototype.render = function() {
        this.m_initStyle();
        this.layer.render();
};

MS.Bricks.prototype.loadData = function(data) {
    this.layer.setData(data, {
        lnglat: 'coordinates',  // 区块的边界点
    });
};





