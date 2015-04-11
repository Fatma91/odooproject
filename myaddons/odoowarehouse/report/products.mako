<html>
    <head>
        <style type="text/css">${css}</style>
    </head>
    <body>
        <h1>Product in the stock </h1><br><br><br>
              <hr>
        % for session in objects:
            <h2>Product ID: ${ session.Proid }</h2>
            <h2>Product Name: ${ session.Pname }</h2>
            <h2>Product Code: ${ session.Procode }</h2>
            <h2>Product Price: ${ session.Price }</h2>
            <h2>Max quantity of Product: ${session.Pmax }</h2>
            <h2>Min quantity of Product: ${session.Pmin}</h2>
        % endfor
    </body>
</html>