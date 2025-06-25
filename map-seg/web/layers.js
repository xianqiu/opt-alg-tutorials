
// 显示砖块
const layerBricks = new MS.Bricks(MS.map);
layerBricks.loadData(MS.data.bricks);
layerBricks.render();

// 显示边界
const layerBlockBoundaries = new MS.Boundaries(MS.map);
layerBlockBoundaries.loadData(MS.data.blockBoundaries);
layerBlockBoundaries.render();


/**
 * 控制图层的显示
 * @param layer{Loca.Layer}
 * @param cb{checkbox}
 */
function ctrlLayer(layer, cb) {
    if (cb.checked) {
        layer.show();
    } else {
        layer.hide();
    }
}