import React, { useState, useEffect } from 'react';
// import '../App.css';
// import {Link} from 'react-router-dom';

function ItemDetail({ match }) {

    useEffect(() => {
        fetchItem();
    },[])

    const [item, setItem] = useState({});

    const fetchItem = async () =>{
        const data = await fetch(`https://reqres.in/api/products/${match.params.id}`);
    
        const item = await data.json();
        console.log(item.data)
        setItem(item.data);
    }

    return (
        <div>
            <h1 key={item.id}>{item.name}</h1>
            <p>Details</p>
            <p>Year: {item.year}</p>
            <p style={{color: item.color}}>Color: {item.color}</p>
            <p>Pantone Value: {item.pantone_value}</p>
        </div>
    );
}

export default ItemDetail;
