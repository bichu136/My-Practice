function setup(){
  createCanvas(3000,3000)
  background(0)
}
let scl=100
let x=0
let y=0
let f1= [0,0,0,0.25,0,-0.4]
let f2= [0.95,0.005,-0.005,0.93,-0.002,0.5]
let f3= [0.035,-0.2,0.16,0.04,-0.09,0.02]
let f4= [0.04,0.2,0.16,0.04,0.083,0.12]
let prop= [2,84,7]
//Barnsley fern;

function draw(){

  translate(1500,1500)
  stroke(255,125,150)
  strokeWeight(1)

  for (var i = 0; i <100; i++) {
    let rand = random(0,100);
    let xtemp=x
    let ytemp=y
    let i=0;
    if(rand<prop[0])                         i=1;
    else if (rand<(prop[0]+prop[1]))         i=2;
    else if(rand <(prop[0]+prop[1]+prop[2])) i=3;
    else                                     i=4;

    switch(i){
      case 1:
      x=f1[0]*xtemp + f1[1]*ytemp + f1[4]
      y=f1[2]*xtemp + f1[3]*ytemp + f1[5]
        point(x*scl,y*scl)
        break;
      case 2:
        x=f2[0]*xtemp + f2[1]*ytemp + f2[4]
        y=f2[2]*xtemp + f2[3]*ytemp + f2[5]
        point(x*scl,y*scl)
        break;
      case 3:
      x=f3[0]*xtemp + f3[1]*ytemp + f3[4]
      y=f3[2]*xtemp + f3[3]*ytemp + f3[5]
        point(x*scl,y*scl)
        break;
      case 4:
        x=f4[0]*xtemp + f4[1]*ytemp + f4[4]
        y=f4[2]*xtemp + f4[3]*ytemp + f4[5]
        point(x*scl,y*scl)
        break;
      default:
    }
  }


}
