/**
 * I'm just preserving a bit of history. My debugging history for the front-
 * end of DLLView.jsx
 * 
 */


//   {/* Matrix grid */}

/* TODO:
 * My notes from Anmol:
 * - Make a grid of flex-columns and flex-rows (absolute position w/in DLLView div)
 * - Make a grid of flex-rows and flex-columns ("")
 * - Layer them in the -SAME- div at the -SAME- absolute position (LOCKED)
 * 
 * In each col/row, make absolute-positioned Nodes.
 * 
 * Horizontal links: absolute-positioned arrow divs (1st layer)
 * - z: ++++ for arrows (nodes can be stacked)
 * Vertical links: absolute-positioned arrow divs (2nd layer)
 * - z: ++++ for arrows
 * 
 * 
 * Helper Algorithms:
 * - Arrow Length calculator
 * - Arrow Position calculator
 * - Edge case handler for the arrows (on the edges lol)
 * 
 * Steps:
 * 1. Find where the bounds of my -ABSOLUTE- positioning is.
 * 2. Create the absolute-positioned Nodes of the initial matrix
 */



    /*
    * Leftmost xPos = 960
    * Topmost yPos = 160
    * 
    * Rightmost xPos = 1920
    * Bottommost yPos = 967   
    * 
    * Mid x: 1440px
    * Mid y:  
    * 
    */
 
// function findArrowPos(posMat, r1, c1, r2, c2, dir) {
//     /* 
//      * There are many "magic numbers" defined in this function. They all
//      * represent offset to align the up, down, left, and right arrows to their
//      * proper location from n1 to n2.
//      * 
//      * These constants were chosen by trial-and-error--a real headache.
//      */


//     console.log("------- New --------")
//     let dr = r2 - r1;
//     let dc = c2 - c1;
//     console.log("r1c1: ", r1, c1, "r2c2: ", r2, c2);


//     let [y1, x1] = posMat[r1][c1];
//     let [y2, x2] = posMat[r2][c2];
//     let [x1Mod, y1Mod, x2Mod, y2Mod] = [0, 0, 0, 0];

//     /* Right Arrow */
//     if (dc > 0 && dir === 'right') {
//         // Connect right side of n1 with left side of n2
//         // console.log("This is a right arrow!");
//         x1Mod = 1 + 47;
//         y1Mod = 25 + 18;
//         x2Mod = -17;
//         y2Mod = 25 + 18;
//     }
//     /* Left Arrow */
//     else if (dc < 0 && dir === 'left') {
//         // Connect left side of n1 with right side of n2
//         // console.log("This is a left arrow!");
//         x1Mod = 2;
//         y1Mod = 25 + 30;
//         x2Mod = 20 + 47;
//         y2Mod = 25 + 30;

//     }
//     /* Down Arrow  */
//     if (dr > 0 && dir === 'down') {
//         if (r2 < r1) { //FIXME: delete
//             console.log("What the heck happened? r2 < r1");
//             x1Mod -= 100;
//         }

//         // Connect bottom of n1 with top of n2
//         console.log("This is a down arrow!");
//         x1Mod = 2 + 30;
//         x2Mod = 2 + 30;
//         y1Mod = 25 + 47;
//         y2Mod = 7;
//     }
//     /* Up Arrow */
//     else if (dr < 0 && dir === 'up') {
        
//         // Connect top of n1 with bottom of n2
//         console.log("This is an up arrow!");
//         x1Mod = 2 + 18;
//         x2Mod = 2 + 18;
//         y1Mod = 26;
//         y2Mod = 90;
//     }

//     if (r2 > r1 && dir === "up") { //FIXME: delete
//         console.log("What the heck happened? r2 > r1");
//         x1Mod += 100;
//     }
//     console.log("Find Arrow Pos: ", [x1+x1Mod, y1+y1Mod, x2+x2Mod, y2+y2Mod], " dir: ", dir);
    
//     return [x1+x1Mod, y1+y1Mod, x2+x2Mod, y2+y2Mod];
// }

 // FIXME: Delete all these johns
    // let [ux1, uy1, ux2, uy2] = findArrowPos(posMat, 1, 0, 0, 0);
    // let [dux1, duy1, dux2, duy2] = findArrowPos(posMat, 2, 0, 0, 0);
    // let [dx1, dy1, dx2, dy2] = findArrowPos(posMat, 0, 0, 1, 0);
    // let [rx1, ry1, rx2, ry2] = findArrowPos(posMat, 0, 0, 0, 1);
    // let [lx1, ly1, lx2, ly2] = findArrowPos(posMat, 0, 1, 0, 0);
    // let [dlx1, dly1, dlx2, dly2] = findArrowPos(posMat, 0, 2, 0, 0);

    /* FIXME: These are the wrapAround tests
    let [eux1, euy1, eux2, euy2] = findArrowPos(posMat, 0, 0, 1, 0, "up");
    let [e2ux1, e2uy1, e2ux2, e2uy2] = findArrowPos(posMat, 0, 1, 2, 1, "up");
    let [e3ux1, e3uy1, e3ux2, e3uy2] = findArrowPos(posMat, 0, 2, 3, 2, "up");

    let [edx1, edy1, edx2, edy2] = findArrowPos(posMat, 1, 0, 0, 0, "down");
    let [e2dx1, e2dy1, e2dx2, e2dy2] = findArrowPos(posMat, 3, 2, 0, 2, "down");
    let [e3dx1, e3dy1, e3dx2, e3dy2] = findArrowPos(posMat, 2, 1, 0, 1, "down");
    */

    let [rx1, ry1, rx2, ry2] = findArrowPos(posMat, 1, 2, 1, 0, "right");
    let [r2x1, r2y1, r2x2, r2y2] = findArrowPos(posMat, 3, 1, 3, 0, "right");
    let [r3x1, r3y1, r3x2, r3y2] = findArrowPos(posMat, 1, 2, 1, 0, "right");
    let [lx1, ly1, lx2, ly2] = findArrowPos(posMat, 1, 0, 1, 2, "left");
    let [l2x1, l2y1, l2x2, l2y2] = findArrowPos(posMat, 2, 1, 2, 2, "left");

    //FIXME: delete these comments
    // console.log("The new posMat poses: ", posMat[0][0], posMat[0][1], posMat[1][0], posMat[1][1]);
    // console.log("The correct arrow poses: ", posMat[0][0][1]+30, posMat[0][0][0]+47, posMat[1][0][1]+30, posMat[1][0][0]);


/**
 * More stuff
 */

<div>
                {/* <SVGArrow key="edge up hardcoded" x1={330} y1={40} x2={330} y2={140}/> Testing hard-coded */}
                {/* <SVGArrow key="edge up" x1={eux1} y1={euy1} x2={eux2} y2={euy2}/>
                <SVGArrow key="edge up 2" x1={e2ux1} y1={e2uy1} x2={e2ux2} y2={e2uy2}/>
                <SVGArrow key="edge up 3" x1={e3ux1} y1={e3uy1} x2={e3ux2} y2={e3uy2}/>
                <SVGArrow key="edge down" x1={edx1} y1={edy1} x2={edx2} y2={edy2} />
                <SVGArrow key="edge down 2" x1={e2dx1} y1={e2dy1} x2={e2dx2} y2={e2dy2} />
                <SVGArrow key="edge down 3" x1={e3dx1} y1={e3dy1} x2={e3dx2} y2={e3dy2} /> */}

                {/* <SVGArrow key="edge l1" x1={lx1} y1={ly1} x2={lx2} y2={ly2} />
                <SVGArrow key="edge l2" x1={l2x1} y1={l2y1} x2={l2x2} y2={l2y2} /> */}
                {/* <SVGArrow key="edge r1" x1={rx1} y1={ry1} x2={rx2} y2={ry2} />
                <SVGArrow key="edge r2" x1={r2x1} y1={r2y1} x2={r2x2} y2={r2y2} /> */}
                {/* <SVGArrow key="edge r3" x1={r3x1} y1={r3y1} x2={r3x2} y2={r3y2} /> */}
            </div>
