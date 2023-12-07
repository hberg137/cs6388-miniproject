import CONSTANTS from 'constants.js';
import Tile from './tile';

export default function Board({player, board, win}) {

    const getTiles = () => {
        const tiles = [];
        board.forEach((index) => {
            console.log(index);
            index.forEach((value, tile) => {
                tiles.push(<Tile key={'tile_' + tile} player={player} piece={value} position={tile} win={win}/>);

            })
        });

        return tiles;
    }

    return (
        <div style={{
            display:'grid',
            gridTemplateColumns: 'repeat(8, 1fr)',
            gap: '0px',
            width: '300px'
        }}>
            {getTiles()}
        </div>
    )
}