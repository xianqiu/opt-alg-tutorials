/**
 * 显示边界
 * @class
 * @param map
 * @constructor
 */
MS.Boundaries = function (map) {
    this.map = map;
    this.layer = new Loca.LineLayer({
        map: map,
        zIndex: 400
    });
};

/**
 * @private
 */
MS.Boundaries.prototype.m_initStyle = function () {
    this.layer.setOptions({
    style: {
        color: '#ff0000',
        borderWidth: 3,
        opacity: 0.3,
    }
});
};

MS.Boundaries.prototype.render = function () {
    this.m_initStyle();
    this.layer.render();
};

MS.Boundaries.prototype.loadData = function (data) {
    this.layer.setData(data, {
        lnglat: 'coordinates'
    });
};
