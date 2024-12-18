
import React from 'react';
import { Card, Button,ProgressBar } from 'react-bootstrap';
import CardGroup from 'react-bootstrap/CardGroup';
import RestLogin from 'react-datta-able-main/react-ui/src/views/forms/Form1course.js';


function GroupExample() {
  return (
    <CardGroup>
      <Card>
        <Card.Img variant="top" src="react-datta-able-main/react-ui/src/email-_1__1.png"/>
        <Card.Body>
          <Card.Title>Курс 1</Card.Title>
          <Card.Text>
          Здесь скоро будет картинка с текстом
          </Card.Text>
          <Button onClick={() => Appform1()} variant="primary">Перейти к курсу</Button>
        </Card.Body>
        <Card.Footer>
         <ProgressBar now={60} />
        </Card.Footer>
      </Card>
      <Card>
        <Card.Img variant="top" src="holder.js/100px160" />
        <Card.Body>
          <Card.Title>Курс 2</Card.Title>
          <Card.Text>
          Здесь скоро будет картинка с текстом{' '}
          </Card.Text>
          <Button variant="primary">Перейти к курсу</Button>
        </Card.Body>
        <Card.Footer>
        <ProgressBar now={60} />
        </Card.Footer>
      </Card>
      <Card>
        <Card.Img variant="top" src="holder.js/100px160" />
        <Card.Body>
          <Card.Title>Курс 3</Card.Title>
          <Card.Text>
          Здесь скоро будет картинка с текстом
          </Card.Text>
          <Button variant="primary">Перейти к курсу</Button>
        </Card.Body>
        <Card.Footer>
        <ProgressBar now={60} />
        </Card.Footer>
      </Card>
    </CardGroup>
  );
}

export default GroupExample;