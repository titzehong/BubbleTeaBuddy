# Bubble Tea Buddy

A telegram chat bot which tells you the nearest bubble tea shop as well as recommends you drinks. 

## Training

Tree based classifiers are used to detect intent of incoming user messages. To train the intent classifier.


## Troubleshooting

### Bot crashes with the unicode error 

If your bot code crashes with the error that ends with `UnicodeEncodeError: 'ascii' codec can't encode character`,
your terminal likely has problems showing unicode symbols. To fix this you can change your terminal local by adding
the following lines to you `~/.bashrc` file (or any other shell configuration):

```
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
```

To verify the effect, you can run the following command end check that it outputs 'utf-8'
```python
> python -c 'import locale; print(locale.getpreferredencoding())'
utf-8
```

You can find more details in this [article](https://perlgeek.de/en/article/set-up-a-clean-utf8-environment).

If this doesn't work, you can explicitly specify the encoding when opening files:
```python
with open(filename, 'r', encoding="utf-8") as file:
  ...
```
