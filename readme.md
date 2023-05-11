> ### migrate SQL queries to Excel

---

1. Copy and update the values

```sh
cp settings.py.template settings.py
```

2. Update or create files inside the `input` folder.


4. Run the following cmd 

- to export de excels inside the `out` directory: 

```sh
make main
```

- to execute custom queries (it can take up to 10min)
```sh
make custom
```

- to execute all
```sh
# TBD 
```

- to zip all files inside the `out` directory: 
```sh
make zip
```