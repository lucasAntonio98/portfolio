// link para acessar o código direto no GEE (entidades presentes) https://code.earthengine.google.com/5a3bbc9124d5593499afb5284a30cf11
// importar base de dados 
var S2 = ee.ImageCollection("COPERNICUS/S2");

// Filtrar imagens 
S2 = S2.filterBounds(area_estudo);
// Filtrar por data
S2 = S2.filterDate("2025-06-01","2025-07-30");
print(S2);

// Abrir a imagem 
var image = ee.Image("COPERNICUS/S2/20250602T132251_20250602T132253_T22KFB");
print(image)

Map.addLayer(image,{min:0,max:3000,bands:"B4,B3,B2"}, "area_estudo");


// Mostrar as bandas selecionadas 
var predictionBands = image.bandNames();
print (predictionBands);

//Preparação das amostrasr
var trainingData = Rios
  .merge(Vegetacao)
  .merge(Agricultura)
  .merge(Solo_e);
 // .merge(Urbana);
print(trainingData)


var classifierTraining = image.select(predictionBands).sampleRegions(
                       {collection: trainingData, 
                         properties: ['land_class'], scale: 20 });

//Treinando classificador 
var classifier =  ee.Classifier.smileRandomForest(300).train({features:classifierTraining, 
                                                    classProperty:'land_class', 
                                                   inputProperties: predictionBands});

// gerar imagem classificada
var classified = image.select(predictionBands).classify(classifier);

var Palette = [
  
  '#0b4a8b', //  rios
  '#0fcf46', // vegetacao
  '#57ff0b', // agricultura
  '#fa1f08', // solo_e
]; 
// validação dos resultados 
var validationData = Acc_rios
  .merge(Acc_vegetacao)
  .merge(Acc_agricultura)
  .merge(Acc_solo_e);

var validation = image.sampleRegions({collection: validationData, properties: ['land_class'], scale:20,tileScale: 16});

var validated = validation.classify(classifier);

// Gerar matriz de confusão, acurácia e Kappa
var testAccuracy = validated.errorMatrix('land_class', 'classification');
print('Validation error matrix: ');
print('Validation overall accuracy: ');
  
  
  



//adicionar imagem classificada no mapa 
Map.addLayer(classified,  {min: 1, max: 5, palette: Palette}, "LULC Area_estudo");
