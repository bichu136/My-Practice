function drawclock(){
  let deg =0;
  background(0);
  translate(200,200);
  while(deg<360){

    let x=16*pow(sin(deg),3);
    let y=13*cos(deg)-5*cos(2*deg)-2*cos(3*deg)-cos(4*deg);

    //stroke(255,150,125);
    //strokeWeight(5);
    //line(0,0,-x,-y);
    stroke(0,0,255);
    strokeWeight(3);
    line(0,-5,-(x*9),-(y*9));
    x=x*10;
    y=y*10;
    if(int(deg)%30==0){
    stroke(255,125,150);
    strokeWeight(10);
    point(-x,-y);
    }
    stroke(255,125,150);
    strokeWeight(3);
    point(-x,-y);

    deg+=0.1;

  }
}
function drawstick(degs,r,b,g){
  let x=16*pow(sin(-degs),3);
  let y=13*cos(-degs)-5*cos(2*-degs)-2*cos(3*-degs)-cos(4*-degs);
  x=(x*9);
  y=(y*9);

  stroke(r,b,g);
  strokeWeight(3);
  line(0,30,-x,-y);
  if(degs%30==0){
    stroke(255,0,0);
    strokeWeight(5);
    point(-x,-y);
  }
}
function setup(){

  createCanvas(400,400);

  angleMode(DEGREES);
  drawclock();
}
function draw(){
  drawclock();
  let sec=second();
  let min=minute()%60;
  let hr=hour()%12;
  let degs=sec*6;
  let degm=min*6;
  let degh=hr*30;
  //draw second stick;
  drawstick(degs,255,150,125);
  drawstick(degh,216,149,95);
  drawstick(degm,130,50,22);
  stroke(255,125,150);
  strokeWeight(10);
  point(0,30);
}
