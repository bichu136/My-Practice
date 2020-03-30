function GreedySearch()
{
  if(current[0] == goal[0] && current[1] == goal[1]){
    console.log("DONE")
    noLoop()
  }
  if (open.length <=0){
    return
  }
  current = open.pop()
  if (grids[current[0]][current[1]].visited){
    return
  }
  let currentDistance = (goal[0] - current[0])+(goal[1]-current[1])
  let upDistance   = -1
  let downDistance = -1
  let leftDistance = -1
  let rightDistance = -1
  let t = []
  let nextgrids = []
  if (grids[current[0]][current[1]].walls["up"] ==false){
    t = goto(current,"up")
    upDistance = abs(goal[0] - t[0])+abs(goal[1]-t[1])
    if(grids[t[0]][t[1]].visited == false)
      nextgrids.push({pos:t,d:upDistance})
  }
  if (grids[current[0]][current[1]].walls["down"] ==false){
    t = goto(current,"down")
    downDistance = abs(goal[0] - t[0])+abs(goal[1]-t[1])
    if(grids[t[0]][t[1]].visited == false)
      nextgrids.push({pos:t,d:downDistance})
  }
  if (grids[current[0]][current[1]].walls["left"] ==false){
    t = goto(current,"left")
    leftDistance = abs(goal[0] - t[0])+abs(goal[1]-t[1])
    if(grids[t[0]][t[1]].visited == false)
      nextgrids.push({pos:t,d:leftDistance})
  }
  if (grids[current[0]][current[1]].walls["right"] ==false){
    t = goto(current,"right")
    rightDistance = abs(goal[0] - t[0])+abs(goal[1]-t[1])
    if(grids[t[0]][t[1]].visited == false)
      nextgrids.push({pos:t,d:rightDistance})
  }
  nextgrids.sort(function(a,b){return b.d-a.d})// if  return <0 then a first return >0 then b first
  console.log(nextgrids)
  grids[current[0]][current[1]].visited = true
  while(nextgrids.length>1)
  {
    open.push(nextgrids.shift().pos)
  }
  open.push(current)
  console.log(nextgrids.length)
  if(nextgrids.length == 1)
    open.push(nextgrids.shift().pos)


}
