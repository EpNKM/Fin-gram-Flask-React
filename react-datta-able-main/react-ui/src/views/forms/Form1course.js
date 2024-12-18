import React from 'react';
import { Formik } from 'formik';


function Appform1() {
    return (
      <div className="App">
        <h1>How are you ?</h1>
        <Formik
          initialValues={{answere: "" }}
          onSubmit={async (values) => {
            await new Promise((resolve) => setTimeout(resolve, 500));
            alert(JSON.stringify(values, null, 2));
          }}
        >
          <Form>
            <Field name="answere" type="text" />
            <button type="submit">Submit</button>
          </Form>
        </Formik>
      </div>
    );
  }
  
  ReactDOM.render(<Appform1 />, document.getElementById("root"));

export default App;
