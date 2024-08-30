import { useState, useEffect } from "react";
import axios from "axios";
import ReactPlayer from "react-player";
import "./App.css";

export default function App() {
  const [videoUrl, setVideoUrl] = useState("");
  const [error, setError] = useState("");
  const [playing, setPlaying] = useState(false); // Состояние для управления воспроизведением

  const fetchVideoUrl = async () => {
    try {
      const response = await axios.get("http://localhost:8000/api/get_video");
      setVideoUrl(response.data);
    } catch (error) {
      setError("Ошибка при загрузке видео");
    }
  };

  useEffect(() => {
    fetchVideoUrl(); // Вызов функции при загрузке компонента
  }, []);

  const handlePlayerClick = () => {
    setPlaying((prevPlaying) => !prevPlaying); // Переключение состояния воспроизведения
  };

  const handleSubscribeClick = () => {
    window.open("https://t.me/daun_type_beat", "_blank"); // Открытие ссылки в новой вкладке
  };

  return (
    <>
      <div className="container">
        <h2>WELCOME TO ROFLSTUDIOS</h2>
        {videoUrl ? (
          <div className="react-player-container" onClick={handlePlayerClick}>
            <ReactPlayer
              url={videoUrl}
              playing={playing} // Управление воспроизведением
              controls={true}
              width="100%"
              height="100%"
            />
          </div>
        ) : (
          <p>{error}</p>
        )}
        <button className="subscribe-button" onClick={handleSubscribeClick}>
          SUBSCRIBE TO US
        </button>
      </div>
    </>
  );
}
