import React, {useCallback, useState} from 'react';
import Board from './board';
import CONSTANTS from 'constants.js';

export default function Othello() {
    {/*
    const getLabel = () => {
        if(!win) {
            let finished = true;
            board.forEach(piece => {
                if(piece === CONSTANTS.PIECE.EMPTY) {
                    finished = false;
                }
            });
            if(finished) {
                return 'Game ended in tie.';
            }
            
            if(player === CONSTANTS.PLAYER.B) {
                return 'Player O moves...';
            } else {
                return 'Player X moves...';
            }
        } else {
            if(win.player === CONSTANTS.PLAYER.B) {
                return 'Player O won!';
            } else {
                return 'Player X won!';
            }
        }
    }
*/}
    return (
    <div style={{ width: '100%', height: '100%', fontFamily:'fantasy', fontSize:'36px', fontWeight:'bold'}}>
        {'test'}
        <Board />
    </div>
    );
}