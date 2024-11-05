from django.shortcuts import get_object_or_404
from django.views import generic
from django.core.mail import send_mail
from . import models, forms, enums


class PostList(generic.ListView):
    """
        Listagem de registros da Model Post, apenas do manager Publicado .

        Por padrão, o context_object_name enviado no contexto é "object_list".
        Sendo necessário alterar, basta definir conforme abaixo:
        context_object_name = 'posts'

        Semelhante ao context, o Django busca, implicitamente, um nome de
        template baseado em [APPNAME]_[VIEW], nesse caso, "post_list".
        Fora desse padrão é necessário explicitar conforme abaixo:
        template_name = 'blog/minha_template_list.html'
    """
    model = models.Post
    queryset = model.publicados.all().order_by('-created_at')
    paginate_by = 2
    allow_empty = True
    context_object_name = 'posts'


class PostDetail(generic.DetailView):
    """
        Retrive do registro obtido.

        Semelhante ao ListView, o Django buscará, implicitamente, uma template
        chamada "post_detail". Fora desse padrão é necessário explicitar
        conforme abaixo:
        template_name = 'blog/minha_template_detail.html'
    """
    model = models.Post


class PostShareView(generic.edit.FormView):
    """
        View para URL de compartilhamento de Post via E-mail
    """
    template_name = 'blog/share.html'
    form_class = forms.EmailForm
    success_url = '.' # Redireciona para a mesma página se bem sucedido

    def dispatch(self, request, *args, **kwargs):
        # armazenar no objeto `self`
        self.post_obj = get_object_or_404(models.Post, pk=kwargs['pk'],
                        status=enums.StatusEnum.published.name)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Obter os dados do formulário
        data = form.cleaned_data
        # build_absolute_uri retorna a URL completa, por isso,
        # não utilizar somente get_absolute_url()
        post_url = self.request.build_absolute_uri(
                                self.post_obj.get_absolute_url())
        subject = f"{data['nome']}"
        message = f"Leia o post {self.post_obj.title} em {post_url}\n\n" \
                  f"Seu comentário: {data['comentario']}"

        send_mail(subject, message, 'admin@admin.com', [data['email']])

        return self.render_to_response(self.get_context_data(
                                                post_url=post_url,
                                                form=form,
                                                sent=True))

    def form_invalid(self, form):
        # recarrega o mesmo formuário
        return self.render_to_response(self.get_context_data(
                                                form=form,
                                                sent=False))

    def get_context_data(self, **kwargs):
        # Incluir p post ao contexto para utilizar no template
        context = super().get_context_data(**kwargs)
        context['post'] = self.post_obj
        return context
