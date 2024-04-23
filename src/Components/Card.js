import React from 'react';
import { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Chip from '@mui/material/Chip';
import axios from "axios";


export default function OutlinedCard() {

  function checkAuthenticity() {
    axios.post('http://127.0.0.1:5000/predict', {news: news_model.news})
            .then((response) => {
                setNewsModel(response.data)
                console.log(response.data)
            })
            .catch((error) => {
                console.log("An error occured while callin the API.")
                throw new Error("An error occured while calling the API. Please check if the server is running. " + error)
            })
  }

  const [news_model, setNewsModel] = useState({
    "news": '',
    "label": ''
  });
  
  const [buttonState, updateButtonState] = useState(true)
  useEffect(() => {
    console.log(news_model)
    if(news_model.news) {
        updateButtonState(false)
    }
    else{
        updateButtonState(true)
    }
  }, [news_model]);
  return (
    <Box sx={{ minWidth: 1000 }}>
      <Card variant="outlined">
        <React.Fragment>
          <CardContent>
                  <TextField
                      id="outlined-multiline-static"
                      label="News"
                      multiline
                      rows={4}
                      defaultValue=""
                      fullWidth
                      onChange={(event) => {
                        setNewsModel({...news_model, news: event.target.value, label: ''});
                      }}
                      />
          </CardContent>
          <CardActions>
            <Button disabled={buttonState} variant='contained' type='submit' onClick={checkAuthenticity}>Check</Button>
            {news_model.label ? <Chip label={news_model.label == "true" ? "True News" : "Fake News"} color={news_model.label == 'true' ? "success" : "error"}/> : null}
          </CardActions>
        </React.Fragment>
      </Card>
    </Box>
  );
}