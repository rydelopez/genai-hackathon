import { useState } from 'react';

const FileUpload = (lesson_id, setFiles, updateFiles) => {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;

    

    const formData = new FormData();
    formData.append('uploaded_file', file);

    try {
      // Update the URL to your upload endpoint

      const response = await fetch(`http://localhost:3500/lesson/pdf?lesson_id=${lesson_id.lesson_id}`, {
        method: "POST", body: formData,
    }).then((res) => res.json());
      console.log('File uploaded successfully', response.data);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
    </div>
  );
};

export default FileUpload;
