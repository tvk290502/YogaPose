import {React,useEffect, useState} from 'react'
import Card from '@mui/material/Card';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button'
import axios from 'axios';

const Yoga = ()=>{
	const [image,setImage] = useState(null);
	const [base64Image,setBase64Image] = useState(null)
	const [analysedImage,setAnalysedImage] = useState(null)
	const [detection,setDetection] = useState(null)

	const onImageChange = (event) => {
		if (event.target.files && event.target.files[0]) {
		  const file = event.target.files[0];
		  const reader = new FileReader();
			reader.onloadend = () => {
				const base64String = reader.result.split(',')[1]; // Extract base64 string from data URL
				setBase64Image(base64String);
			};
			reader.readAsDataURL(file);
		  setImage(URL.createObjectURL(event.target.files[0]));
		}
	       }

	const analyse =  () =>{
		axios.post('http://127.0.0.1:5000/detect',{'img': base64Image})
		.then(res=>{
			console.log(res['data']['inputImg'])
			setAnalysedImage(res['data']['img'])
			setDetection(res['data']['prediction'])
			setBase64Image(res['data']['inputImg'])
		})
	}

	return(
		<div>
			<div style={{display:'flex'}} >
				<div style={{width:'45%', margin:'auto'}} >
					<Card sx={{ maxWidth: '100%' }}>
						<img style={{width:'95%', height:'95%', margin:'auto', borderRadius:'5px'}} src = {`data:image/jpeg;base64,${base64Image}`} />
					</Card>

				</div>

				<div style={{width:'45%', margin:'auto'}} >

					<h2>Pattern pose for reference</ h2>
					
					<Card sx={{ maxWidth: '100%' }}>
						<img style={{width:'95%', height:'95%', margin:'auto', borderRadius:'5px'}} src = {`data:image/jpeg;base64,${analysedImage}`}/>
					</Card>

				</div>
			
			</div>
			<div>
				{detection!== null && <h5>Detected position: {detection} </h5> } 
			</div>
			<div style={{marginTop:'30px'}} >
			<input
				accept="image/*"
				id="contained-button-file"
				onChange={onImageChange}
				multiple
				type="file"
				style={{display:'none'}}
			/>
		
			<label htmlFor="contained-button-file">
				<Button variant="contained" color="primary" component="span">
				Upload
				</Button>
			</label>
			
			<Button onClick={analyse} sx={{marginLeft:'30px'}} variant="contained" color="primary" component="span" >
				Analyze
			</Button>
			</div>
    

		</div>
	)
}

export default Yoga