/**
 * Traveling salesman tour
 * @class
 * @param map
 * @constructor
 */
S.Tour = function (map) {
    this.layer = new Loca.LinkLayer({
        map: map,
        fitView: true
    });
};

/**
 * @private
 */
S.Tour.prototype.m_initStyle = function () {
    this.layer.setOptions({
    style: {
        color: '#ff910f',
        borderWidth: 2,
        opacity: 0.8,
    }
});
};

S.Tour.prototype.render = function () {
    this.m_initStyle();
    this.layer.render();
};

S.Tour.prototype.loadData = function (data) {
    this.layer.setData(data, {
        lnglat: 'line'
    });
};

