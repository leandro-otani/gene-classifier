function transpose(data){

  labels = ["Class","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MED","MGL","MGL","MGL","MGL","MGL","MGL","MGL","RHB","RHB","RHB","RHB","RHB","RHB","RHB","EPD","EPD","EPD","EPD","EPD","EPD","EPD","EPD","EPD","EPD","JPA","JPA","JPA","JPA","JPA","JPA"];

  csv = "data:text/csv;charset=utf-8,";

  csv = csv + "Class,";
  for( j= 1; j <= data.length; j++){
      csv = csv + "at"+j;
      if(j <= data.length - 1)
        csv = csv+",";
  }
  csv = csv + "\n";

  for(i=1; i<= 69; i++){
    csv = csv + labels[i]+",";
    for( j= 0; j < data.length; j++){
      csv = csv + data[j].split(",")[i];
      if(j < data.length - 1)
        csv = csv+",";
    }
    csv = csv + "\n";


  }
  var encodedUri = encodeURI(csv);
    window.open(encodedUri);
  console.log(csv);
}