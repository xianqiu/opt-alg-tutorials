// 显示小店
const layerCities = new S.Leads(S.map);
layerCities.loadData(S.data.cities);
layerCities.render();

// 显示tour
const layerTour = new S.Tour(S.map);
layerTour.loadData(S.data.tour);
layerTour.render();