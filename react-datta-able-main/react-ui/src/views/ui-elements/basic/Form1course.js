import React, { useState } from 'react';
import { Formik, Field, Form, ErrorMessage } from 'formik';
import 'bootstrap/dist/css/bootstrap.min.css';

const Example = () => {
  const [result, setResult] = useState(null); // Состояние для хранения результата

  return (
    <div className="container mt-5">
      <h1>С чем работает Excel?</h1>
      <Formik
        initialValues={{
          picked: '',
        }}
        validate={values => {
          const errors = {};
          if (!values.picked) {
            errors.picked = 'Пожалуйста, выберите один из вариантов.';
          }
          return errors;
        }}
        onSubmit={async (values) => {
          await new Promise((r) => setTimeout(r, 500));
          
          // Проверка результата
          const isCorrect = values.picked === 'Таблица';
          const message = isCorrect ? 'Правильно!' : 'Неправильно. Правильный ответ: Таблица.';
          
          // Создание объекта результата
          const resultObject = {
            picked: values.picked,
            isCorrect,
            message,
          };

          // Установка результата в состояние
          setResult(resultObject);
          
          // Вывод результата в консоль
          console.log(JSON.stringify(resultObject, null, 2));
        }}
      >
        {({ values }) => (
          <Form>
            <div className="form-group">
              <label id="my-radio-group">Выбрано</label>
              <div role="group" aria-labelledby="my-radio-group">
                <div className="form-check">
                  <Field type="radio" name="picked" value="Таблица" className="form-check-input" />
                  <label className="form-check-label">Таблица</label>
                </div>
                <div className="form-check">
                  <Field type="radio" name="picked" value="Текстовый документ" className="form-check-input" />
                  <label className="form-check-label">Текстовый документ</label>
                </div>
                <div>Выбрано: {values.picked}</div>
              </div>

              {/* Отображение ошибки */}
              <ErrorMessage name="picked" component="div" className="text-danger mt-2" />
            </div>

            <button type="submit" className="btn btn-primary">Подтвердить</button>
          </Form>
        )}
      </Formik>

      {/* Отображение результата на странице */}
      {result && (
        <div className="mt-4">
          <h3>Результат:</h3>
          <div className="card">
            <div className="card-body">
              <pre>{JSON.stringify(result, null, 2)}</pre>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Example;