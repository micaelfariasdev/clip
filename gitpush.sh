#!/bin/bash

# Verifica se foi passado um parâmetro
if [ -z "$1" ]; then
  echo "Uso: ./gitpush.sh \"mensagem do commit\""
  exit 1
fi

# Executa os comandos git
git add .
git commit -m "$1"
git push
