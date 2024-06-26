import React, {useCallback, useState} from 'react';
import Board from './board';
import CONSTANTS from 'constants.js';

export default function Othello({player, counts, win, board}) {
    const getLabel = () => {
        if(!win) {
            let finished = false;
            board.forEach(piece => {
                if(piece === CONSTANTS.PIECE.EMPTY) {
                    finished = false;
                }
            });
            if(finished) {
                return 'Game ended in tie.';
            }
            
            console.log(counts["whiteCount"])
            if(player === "black") {
                var str = 'Player black moves... ';
                str = str.concat("black count: ", counts["blackCount"], ", white count: ", counts["whiteCount"]);
                return str;
            } else {
                var str = 'Player white moves... ';
                str = str.concat("white count: ", counts["whiteCount"], ", black count: ", counts["blackCount"]);
                return str;
            }
        } else {
            if(win.player === "black") {
                return 'Player black won!';
            } else {
                return 'Player white won!';
            }
        }
    }
    return (
    <div style={{ width: '100%', height: '100%', fontFamily:'fantasy', fontSize:'36px', fontWeight:'bold'}}>
        {getLabel()}
        <Board player={player} board={board} win={win}/>
    </div>
    );
}