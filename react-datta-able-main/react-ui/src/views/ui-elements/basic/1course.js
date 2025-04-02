import React from 'react';
import { useHistory } from "react-router-dom";
import {Button} from 'react-bootstrap';



const ExcelInfo = () => {
  const history = useHistory();
  
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Информация об Microsoft Excel</h1>
      <p>
        Microsoft Excel — это электронная таблица, разработанная компанией Microsoft для
        операционных систем Windows, macOS, Android и iOS. Она является частью пакета
        Microsoft Office и используется для обработки данных, анализа и визуализации.
      </p>
      
      <h2>Основные функции Excel:</h2>
      <ul>
        <li>Создание и редактирование таблиц.</li>
        <li>Формулы и функции для вычислений.</li>
        <li>Графики и диаграммы для визуализации данных.</li>
        <li>Сортировка и фильтрация данных.</li>
        <li>Условное форматирование для выделения важных данных.</li>
      </ul>

      <h2>Применение Excel:</h2>
      <p>
        Excel широко используется в различных областях, включая:
      </p>
      <ul>
        <li>Финансовый анализ</li>
        <li>Управление проектами</li>
        <li>Анализ данных</li>
        <li>Отчеты и презентации</li>
      </ul>

      <h2>Дополнительные ресурсы:</h2>
      <p>
        Пройти тестирование:
      </p>
      <Button onClick={() => history.push('/basic/Form1cource')} variant="primary">Перейти к курсу</Button>
    </div>
  );
};

export default ExcelInfo;