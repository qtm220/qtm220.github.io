# Encryption Set Up

1. Install PageCrypt

```
npm i -D pagecrypt  
```

2. Create Password
```
npx pagecrypt index.html encrypted-index.html -g 256
```
outputs this key, which I use in the github workflow to encrypt solutions
```
ENCRYPTION_KEY="WdHXFuNAA7HQVtn1BDDY3EEOMaShYf5ruZJxVfjFwGOBlFRIemiMBfRkJYDayRxc34dA3HcmFYhBdoFp6KuPyOzypFIhi2Prw1X6gcgYRlKrdz9RHpNySzvHT1NqViCagzSHJgcamyDuKlTZbAM9OFYDykLjOuPoxDDwd20q0jkcJeeza5StMMTKKJ3RIompZBlksW8bsFbcEGgnxQwimsrsSNxaqItpodVzn422zFwfAZENDtUwrXkH6C75c9vv
```

3. Use: see workflow


