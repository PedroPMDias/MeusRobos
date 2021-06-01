<!DOCTYPE html>
<html lang="pt-br">
    <head>
        <title>Definições da minha API</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </head>
    <body>
        <div class="jumbotron jumbotron-fluid">
            <div class="container text-white bg-info">
                <h1>Definições da minha API de análise de dados do clima</h1>
                <h2>Esta API é um protótipo de um projeto que eu sempre tive vontade de construir, por um objetivo pessoal e sem conexão direta com tecnologia, que era de saber como seria o clima de um lugar que eu estivesse.</h2>
                <p>Na construção dessa API, eu quis pensar nela como uma função que fará parte de uma biblioteca de APIs para trazer informações da internet de sites específicos que farão parte de um outro projeto que ainda está no papel por enquanto, mas em breve estará aqui no GitHub também. Em breves detalhes, o que eu pretendo fazer é um App de gestão pessoal para alunos de uma universidade. Nesse app, os alunos poderão acessar as informações dele(a), do curso, da instituição, das dependências da instituição, entre várias outras e com diversas finalidades.</p>
                <p>Uma destas finalidades será a tela de boas-vindas do usuário, que ficará na Home deste App, e uma das informações de consulta disponíveis será a de previsão do clima. Eu ainda estou planejando como serão dispostas estas informações, por isso pensei num esquema ainda simples que fará a raspagem das informações do clima de uma cidade, e montará um organograma do clima para aquela localidade num arquivo estático em HTML.</p>
                <small>Os dados de entrada desta API serão 2 strings contendo os nomes de cidade e estado daquela localidade, sendo que para a cidade poderá haver espaços entre seus nomes, e o estado deverá ser na forma de sigla. Exemplo, cidade = "rio de janeiro" e estado = "rj".</small>
                <p>A saída será apenas a confirmação da criação deste arquivo HTML, caso ele já exista, a API não será executada e será retornada esta informação tratada para o usuário, mas apenas por questões didáticas, porque depois de ter concluído todas as operações que eu quero fazer, não terá mais sentido uma mensagem de retorno, pois o que eu quero é que apenas ela não execute e não retorne nada. O único usuário que precisa saber dos erros e retornos, por enquanto, sou eu kkkkk.</p>
                <p>A estrutura da API será toda condensada no arquivo main.py dentro da pasta /ClimaTempo. No arquivo tem uma função única que receberá as 2 strings como entrada, juntamente com a importação dos objetos de classe que farão todo o processamento dessas informações. Essa informação será sempre constante, pois ainda estou considerando os casos em que alunos podem apenas estar em uma única cidade durante a conclusão do curso.</p>
                <small>Para os casos de mudança de endereço permanecendo na mesma instituição, a mudança será feita nos dados de endereço do usuário e da nova localidade, através de outra API da mesma biblioteca, mas que será desenvolvida em outro momento.</small>
                <p>A função do arquivo main.py fará a verificação da existência dos dados do clima daquela localização que estarão armazenados em um arquivo JSON que terá outra finalidade ainda não bem explícita dentro deste mesmo projeto. Neste JSON só serão salvas as urls de acesso ao site para a raspagem dos dados do clima, estando agrupadas na forma de chave e valor, sendo a chave o nome da página obtida através da tag <code> <title> </code>, e o valor é a url respectiva àquela página.</p>
                <p>Se o JSON estiver vazio, será executada uma função independente que pesquisará no Google por estas urls e retornará um objeto dict que será salvo no arquivo JSON e depois continuará o processamento. Caso ele exista, o JSON será desmembrado para que seja feita uma raspagem personalizada sobre cada página, mas que no final do fluxo, será criado apenas um arquivo HTML condensado contendo todas as informações.</p>
            </div>
        </div>
    </body>
</html>