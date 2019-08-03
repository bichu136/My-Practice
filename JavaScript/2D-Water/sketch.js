let cur= [];
let prev=[];
let damping = 0.7;
let w = 1;
function setup(){
  createCanvas(200,200);

      //mousePressed(press())
      for (var i = 0; i < 200; i++) {
        for (var j =0; j <200; j++) {
          cur[i*200 + j]=0;
          prev[i*200 + j]=0;
        }
      }
}
function mousePressed()
{
  cur[mouseX*200 + mouseY]=255;
}
function draw(){
  background(126)

  for (var i = 1; i < 199; i++) {
    for (var j = 1; j <199; j++) {
      prev[i*200 + j] = (cur[(i+w)*200 + j]+
                 cur[(i-w)*200 + j]+
                 cur[i*200 + j+w]+
                 cur[i*200 + j-w])/2 - prev[i*200 + j];
      prev[i*200 + j]*= damping;
      if(prev[i*200+j]>0){
      stroke(0,0,prev[i*200 + j])
      point(i,j)
      }
    }
  }
    let temp= prev;
    prev= cur;
    cur = temp;
    //console.log(cur)
    //console.log(temp)
    stroke(255,0,0)
    strokeWeight(2)
    //point(250,250)
}
