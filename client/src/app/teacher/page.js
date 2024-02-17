'use client';

import { Card, Metric, Text, Title, BarList, Flex, Grid } from '@tremor/react';
import { Upload } from 'react-feather';
import FileUpload from './upload';
import { useEffect } from 'react';
import FileList from './files';
import { useState } from 'react';
import React from 'react'
import Select from "react-select";



  
  




export default function Teacher() {

    const [files, setFiles] = useState([
    ]);

    const [lesson, setLesson] = useState({label: "", value: 1});
    const [name, setName] = useState("");

    const [conversations, setConversations] = useState([
    ]);



    const updateFiles = async() => {
        const response = await fetch(`http://localhost:3500/lesson/${lesson.value}`
        ).then((res) => res.json());
        setFiles(response.uploads);
    };

    const setConvos = async() => {
        const response = await fetch(`http://localhost:3500/lessons/${lesson.value}`
        ).then((res) => res.json());
        setConversations(response);
    };

    useEffect(() => {
        updateFiles();
        setConvos();
    }, []);

    useEffect(() => {
        updateFiles();
    }, [lesson]);


    const handleSubmit = async() => {
        
        const response = await fetch(`http://localhost:3500/lesson?instructor_id=${1}&description=${name}`, {
            method: "POST"
           
        }
        ).then((res) => res.json());
        setName(name);
        setLesson({"value": response.id, "label": name});
        setConversations([...conversations, {value: response.id, label: name}])
    };


    const handleDelete = async(fileName) => {
        setFiles(files.filter(file => file.name !== fileName));
        const response = await fetch(`http://localhost:3500/lesson/${1}`
        ).then((res) => res.json());
        
    };

    
    return (
        <>

        <>
        <>
        <Select
        defaultValue={lesson}
        onChange={setLesson}
        options={conversations}
      />
      <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', maxWidth: '500px', width: '100%' }}>
        <h2>Create Lesson</h2>
        <div>
        <label>Name:</label>
        <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
        </div>
        <button onClick={handleSubmit}>Submit</button>
      </div>
      </>
        <FileUpload lesson_id={lesson.value} setFiles={setFiles} updateFiles={updateFiles}/>
        
        </>
        
        <FileList files={files} onDelete={handleDelete} />
        
        </>
    );
}


