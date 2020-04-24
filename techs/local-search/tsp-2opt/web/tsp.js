/**
 * 命名空间
 * @class
 * @abstract
 */
var S = S || {};

/**
 * 数据的命名空间
 * @class
 * @abstract
 */
S.data = {};

/**
 * 高德地图对象
 */
S.map = new AMap.Map('container', {
            mapStyle: 'amap://styles/1de318cbb8d12c02303a22c550b9ccc9',
            pitch: 0,
            features: ['bg', 'road'],
            zoom: 10,
            viewMode: '2D'
});


/***********
 * 项目文件 *
 ***********/

// 城市图层
document.write("<script type='text/javascript' src='data_cities.js' charset='UTF-8'></script>");
document.write("<script type='text/javascript' src='cities.js' charset='UTF-8'></script>");

// Tour图层
document.write("<script type='text/javascript' src='data_tour.js' charset='UTF-8'></script>");
document.write("<script type='text/javascript' src='tour.js' charset='UTF-8'></script>");

// 所有图层的展示
document.write("<script type='text/javascript' src='layers.js' charset='UTF-8'></script>");