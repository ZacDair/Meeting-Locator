function aStar(origin, destination, cells){

    //Cells that make up the path
    let pathResult = [];

    //List of cells that have been explored but who's neighbour's have not (Format: [{CellA, f},...])
    let openCells = [];

    //List of cells that have been explored & who's neighbour's are in the open list (Format: [{CellA, f},...])
    let closedCells = [];

    //Variable to track our current position
    let currentPos = null;

    //Add the origin to the open list with a total distance of 0
    openCells.push({cell:origin,f:0});

    //Run until openCells is empty, initial run will use the origin as the current cell
    while(openCells.length !== 0) {

        //Find the lowest total distance value in the open cells
        let lowestF;
        let i = 0;
        let x;
        let cellIndex = -1;
        for (x of openCells) {
            if (i === 0) {
                lowestF = x.f;
                currentPos = x.cell;
                cellIndex = i;
            } else {
                if (x.f < lowestF) {
                    lowestF = x.f;
                    currentPos = x.cell;
                    cellIndex = i;
                }
            }
            i = i + 1;
        }


        //If the id of the current position and the destination match exit and return the result
        console.log("pos:", currentPos[0]);
        console.log("destination:", destination[0]);
        if (currentPos[0] === destination[0]) {
            console.log("We are path done finding");
            return pathResult;
        }

        //Get our current distance to the destination - heuristic (line distance)
        //Distance variables in context of A* conventions
        //f = g + h
        //g = movement cost from start to current node using the path
        //h = estimated distance from the node to the end (heuristic)
        //g = currentPathCost
        //h = distanceToGoal

        //let currentDistance = findDistance(currentPos, destination);
        let currentPathCost = findCurrentPathDistance(pathResult, 10);
        let distanceToGoal = findDistance(currentPos, destination);
        let currentTotal = currentPathCost + distanceToGoal;
        console.log("currentPathCost: ",currentPathCost);
        console.log("distanceToGoal: ",distanceToGoal);
        console.log("currentPathCost: ",currentTotal);

        // Remove current cell from open list and add it to closed
        openCells.splice(cellIndex, 1);
        closedCells.push({cell: currentPos, f: currentTotal});

        //Get our neighbours
        let neighbours = getNeighbours(currentPos, cells, true, 10);
        if (neighbours.length === 0) {
            console.log("Exiting as there was no neighbours to check...");
            return pathResult;
        }
        //For each neighbour
        let neighbour;
        let cellDistancePairs = {};
        for (neighbour of neighbours) {

            //Get the distance from current pos to them (distance A) using the current path
            let distanceA = findCurrentPathDistance(pathResult, 10);

            //Get the distance from them to goal (distance B)
            let distanceB = findDistance(neighbour, destination);

            //Store the cell and total distance as a key pair
            let totalDistance = (distanceA + 10) + distanceB;
            cellDistancePairs[neighbour] = totalDistance;

            //Check if the neighbour is in the open list
            if (isCellInList(neighbour, openCells)) {
                if (totalDistance <= currentTotal) {
                    closedCells.push({cell: currentPos, f: currentTotal});
                }
            } else if (isCellInList(neighbour, closedCells)) {
                if (totalDistance <= currentTotal) {
                    closedCells.push({cell: currentPos, f: currentTotal});
                }
                closedCells.splice(findCellIndexByID(neighbour, closedCells), 1);
                openCells.push({cell: neighbour, f: totalDistance});
            } else {
                openCells.push({cell: neighbour, f: totalDistance});
            }
        }
        pathResult.push(currentPos);

    }
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
function runAlgorithm(origin, destination, cells){
    console.log("Running test algo");
    //Run the removeWalls function on our cells sent from html page
    let floorCells = removeWalls(cells);

    //Extract the index from the rect id example: (Rect-9193) where 9193 is the index
    let originCell = cells[origin.slice(5,origin.length)];
    let destinationCell = cells[destination.slice(5,origin.length)];
    console.log("origin:",originCell);
    console.log("destination:",destinationCell);
    let res = aStar(originCell, destinationCell, floorCells);
    drawPath(res);
    console.log("res: ",res);
    console.log("path should now be drawn");
}


//Get cell neighbours - Cell [ID, X, Y, Color] - (code could be cleaner loop altering the properties)
function getNeighbours(cell, cells, diagonals, cellWidth){
    let neighbours = [];
    //Top
    let temp = findCellByCoords(cell[1], cell[2]+cellWidth, cells);
    if(temp !== null){
        neighbours.push(temp);
    }
    //Bottom
    temp = findCellByCoords(cell[1], cell[2]-cellWidth, cells);
    if(temp !== null){
        neighbours.push(temp);
    }
    //Right
    temp = findCellByCoords(cell[1]+cellWidth, cell[2], cells);
    if(temp !== null){
        neighbours.push(temp);
    }
    //Left
    temp = findCellByCoords(cell[1]-cellWidth, cell[2], cells);
    if(temp !== null){
        neighbours.push(temp);
    }
    //If diagonals are allowed
    if(diagonals) {
        //Top - Right
        temp = findCellByCoords(cell[1]+cellWidth, cell[2]+cellWidth, cells);
        if(temp !== null){
            neighbours.push(temp);
        }
        //Top - Left
        temp = findCellByCoords(cell[1]+cellWidth, cell[2]-cellWidth, cells);
        if(temp !== null){
            neighbours.push(temp);
        }
        //Bottom - Right
        temp = findCellByCoords(cell[1]-cellWidth, cell[2]+cellWidth, cells);
        if(temp !== null){
            neighbours.push(temp);
        }
        //Bottom - Left
        temp = findCellByCoords(cell[1]-cellWidth, cell[2]-cellWidth, cells);
        if(temp !== null){
            neighbours.push(temp);
        }
    }
    console.log(neighbours.length);
    return neighbours;
}

//Find a cell with the same x and y as required if not found return null
function findCellByCoords(x, y, cells){
    let cell;
    for (cell of cells){
        if(cell[1] === x && cell[2] === y){
            return cell;
        }
    }
    return null;
}

//Find a cell based on its ID
function findCellIndexByID(cell, cells){
    let cellID = cell[0];
    let x;
    let index = 0;
    for (x of cells){
        if(x.cell[0] === cellID){
            return index;
        }
        index = index + 1;
    }
    return null;
}

//Find a cell in the open list
function isCellInList(cell, list){
    let x;
    for (x of list){
        if(cell === x.cell){
            return true;
        }
    }
    return false;
}

//Find distance between two cells (returns integer value)
function findDistance(cellA, cellB){
    //Use distance formula between two points sqrt((x2 − x1)^2 + (y2 − y1)^2)
    return Math.sqrt(Math.pow((cellB[1]-cellA[1]), 2) + Math.pow((cellB[2]-cellA[2]), 2));
}

//Find distance using the generated path
function findCurrentPathDistance(currentPath, cellWidth){
    if(currentPath.length !== 0) {
        return currentPath.length * cellWidth;
    }
    else{
        return 0;
    }
}

//Convert a string of values into the array that matches the cell format (including int datatypes for coords)
function splitKeyIntoVals(key){
    let temp = key.split(",");
    temp[1] = parseInt(temp[1]);
    temp[2] = parseInt(temp[2]);
    return temp;
}

//Draw our path
function drawPath(pathCells){
    let cell;
    for(cell of pathCells){
        let temp = document.getElementById("rect-"+cell[0]);
        temp.style.fill = "#00FFFF";
    }
}