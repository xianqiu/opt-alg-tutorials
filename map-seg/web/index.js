/**
 * 命名空间
 * @class
 * @abstract
 */
var MS = MS || {};

/**
 * 数据的命名空间
 * @class
 * @abstract
 */
MS.data = {};

/**
 * 高德地图对象
 */
MS.map = new AMap.Map('container', {
            mapStyle: 'amap://styles/1de318cbb8d12c02303a22c550b9ccc9',
            pitch: 0,
            features: ['bg', 'road'],
            zoom: 10,
            viewMode: '2D'
});


/***********
 * 项目文件 *
 ***********/

// 砖块图层
document.write("<script type='text/javascript' src='data_bricks.js' charset='UTF-8'></script>");
document.write("<script type='text/javascript' src='bricks.js' charset='UTF-8'></script>");

// 边界图层
document.write("<script type='text/javascript' src='data_boundaries.js' charset='UTF-8'></script>");
document.write("<script type='text/javascript' src='boundaries.js' charset='UTF-8'></script>");

// 展示所有图层
document.write("<script type='text/javascript' src='layers.js' charset='UTF-8'></script>");