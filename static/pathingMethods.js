function aStar(origin, destination, cells){
    let pathResult = [];
    /*
    let openCells = [];
    let closedCells = [];
    openCells.push(origin);
    while(openCells){
        let currentPos = openCells[openCells.length];
        if (currentPos === destination){
            console.log("Path Found");
            return pathResult;
        }
        closedCells.push(currentPos);
    }
    */
    console.log(getNeighbours(origin, cells,true));
    console.log(getNeighbours(cells[1], cells,true));
    console.log(getNeighbours(cells[2], cells,true));

    return pathResult;
}

// Function removes any walls from the list as they aren't viable cells
function removeWalls(cells){
    let viableCells = [];
    let cell;
    for(cell of cells){
        //Check if the color section of the cell is white (ie a floor cell)
        if(cell[3] === "#FFFFFF"){
            viableCells.push(cell);
        }
    }
    return viableCells;
}

// function used as main currently
function debug(origin, destination, cells){
    console.log("Running test algo");

    //Run the removeWalls function on our cells sent from html page
    let floorCells = removeWalls(cells);

    //Extract the index from the rect id example: (Rect-9193) where 9193 is the index
    let originCell = cells[origin.slice(5,origin.length)];
    let destinationCell = cells[destination.slice(5,origin.length)];

    console.log("origin:",originCell);
    console.log("destination:",destinationCell);
    let res = aStar(originCell, destinationCell, floorCells)
}


//Get cell neighbours - Cell [ID, X, Y, Color]
function getNeighbours(cell, cells, diagonals){
    let neighbours = [];
    //Top
    let temp = findCellInList(cell, cell[1], cell[2]+10, cells);
    if(temp !== null){
        neighbours.push(temp);
    }
    //Bottom
    temp = findCellInList(cell, cell[1], cell[2]-10, cells);
    if(temp !== null){
        neighbours.push(temp);
    }
    //Right
    temp = findCellInList(cell, cell[1]+10, cell[2], cells);
    if(temp !== null){
        neighbours.push(temp);
    }
    //Left
    temp = findCellInList(cell, cell[1]-10, cell[2], cells);
    if(temp !== null){
        neighbours.push(temp);
    }
    //If diagonals are allowed
    if(diagonals) {
        //Top - Right
        temp = findCellInList(cell, cell[1]+10, cell[2]+10, cells);
        if(temp !== null){
            neighbours.push(temp);
        }
        //Top - Left
        temp = findCellInList(cell, cell[1]+10, cell[2]-10, cells);
        if(temp !== null){
            neighbours.push(temp);
        }
        //Bottom - Right
        temp = findCellInList(cell, cell[1]-10, cell[2]+10, cells);
        if(temp !== null){
            neighbours.push(temp);
        }
        //Bottom - Left
        temp = findCellInList(cell, cell[1]-10, cell[2]-10, cells);
        if(temp !== null){
            neighbours.push(temp);
        }
    }
    return neighbours;


}
// Find a cell with the same x and y as required if not found return null
function findCellInList(currentCell, x, y, cells){
    let cell;
    for (cell of cells){
        if(cell[1] === x && cell[2] === y){
            return cell;
        }
    }
    return null;
}