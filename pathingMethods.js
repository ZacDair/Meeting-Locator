function djikstra(origin, destination, cells){
    let pathResult = [];


    return pathResult;
}

// Function removes any walls from the list as they aren't viable cells
function removeWalls(cells){
    let viableCells = [];
    for (let cell in cells){
        //Check if the color section of the cell is white (ie a floor cell)
        if(cell[0] === "#FFFFFF"){
            viableCells.push(cell);
        }
    }
    return viableCells;
}

export function debug(cells){
    let res = removeWalls(cells);
    for (let x in res){
        console.log(x)
    }
}