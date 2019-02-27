class circles
{
  constructor(x,y,r,stRad,spd,Parent){
    this.x=x;
    this.y=y;
    this.r=r;
    this.spd=spd;
    this.stRad=stRad;
  }
}

class Point{
  constructor(x,y){
    this.x=x;
    this.y=y;
  }
}
function setup(){
  createCanvas(4000,4000);
  angleMode(RADIANS);
  int
  Initialize(cirs,n)
}

//setting up


let wave= [] ;
let cirs = [];
let n=4
function Initialize(cirs,n){
  cirs.push(new circles(0,0,175,-HALF_PI,0.05))

  for (var i = 1; i < n; i++) {
    cirs.push(new circles(0,0,cirs[i-1].r*0.5,-HALF_PI,cirs[i-1].spd*1.5))
  }
  //-----heart shape 1------//
  // n=4 r*0.5 Ospeed=0.1 ratioSpeed 1.5 //
}
function draw(){
  translate(2000,2000);
  background(0);
  stroke(255);
  strokeWeight(2);
  noFill()

  point(cirs[0].x,cirs[0].y)
  ellipse(cirs[0].x,cirs[0].y,cirs[0].r*2,cirs[0].r*2)
  //cirs[0].stRad=cirs[0].stRad+cirs[0].spd
  //cirs[0].x=cirs[0].r*cos(cirs[0].stRad)
  //cirs[0].y=cirs[0].r*sin(cirs[0].stRad)
  let temp=0
  for (var i = 1; i < n; i++) {

    cirs[i].stRad=cirs[i].stRad+cirs[i].spd
    temp=cirs[i-1].r+cirs[i].r
    cirs[i].x=cirs[i-1].x+temp*cos(cirs[i].stRad)
    cirs[i].y=cirs[i-1].y+temp*sin(cirs[i].stRad)
    stroke(255);
    ellipse(cirs[i].x,cirs[i].y,cirs[i].r*2)
    stroke(255,0,0)
    //noLoop()
    point(cirs[i].x,cirs[i].y)
    //print(cirs[i].x,cirs[i].y)
    //noLoop()
    //point(cirs[i].x,cirs[i].y)
    if(i+1==n){
      //line(cirs[i].x,cirs[i].y,0,cirs[i].y)
      wave.unshift(new Point(cirs[i].x,cirs[i].y))

    }

  }
  //translate(200,0)
  beginShape()
  for(var i=0;i<wave.length;i++){
    vertex(wave[i].x,wave[i].y)
  }
  endShape()
  //for(var i=0;i<wave.length;i++){
  //  point(wave[i].x,wave[i].y)
  //}

  //stroke(255,0,0);
  //strokeWeight(2);
  //let y=r*sin(a*deg);
  //wave.unshift(y);
  //beginShape();
  //fill(0,0,0);
  //for (let i = 0; i < wave.length; i++) {
  //  vertex(i,wave[i]);
  //}
  //endShape();
}
