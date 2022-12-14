import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.views.generic import ListView

from app.forms import WorkerCreationForm, CreateTaskForm, UpdateTaskForm
from app.models import Task, Worker, TaskType, Position


@login_required
def complete_task(request, pk):
    pass


@login_required
def index(request):
    """View function for the home page of the site."""

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    queryset = Task.objects.all().select_related()

    if request.GET.get("name") is not None:
        queryset = queryset.filter(name__icontains=request.GET.get("name"))

    context = {
        "tasks": queryset,
        "priorities": [priority[1] for priority in Task.PRIORITY_CHOICES],
        "workers_without_user": Worker.objects.exclude(id=request.user.id).select_related(),
        "task_types": TaskType.objects.all(),
    }

    return render(request, "app/index.html", context=context)


class CriticalTaskListView(LoginRequiredMixin, generic.ListView):
    """ListView class only for critical tasks."""

    model = Task
    template_name = "app/critical_task_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CriticalTaskListView, self).get_context_data(**kwargs)
        user = self.request.user
        critical_tasks = Task.objects.filter(priority="Critical", assignees=user).select_related()

        if self.request.GET.get("name") is not None:
            critical_tasks = critical_tasks.filter(name__icontains=self.request.GET.get("name"))

        context["critical_tasks"] = critical_tasks

        return context


class ImportantTaskListView(LoginRequiredMixin, generic.ListView):
    """ListView class only for important tasks."""

    model = Task
    template_name = "app/important_task_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ImportantTaskListView, self).get_context_data(**kwargs)
        user = self.request.user
        important_tasks = Task.objects.filter(priority="Important", assignees=user).select_related()

        if self.request.GET.get("name") is not None:
            important_tasks = important_tasks.filter(name__icontains=self.request.GET.get("name"))

        context["important_tasks"] = important_tasks

        return context


class NormalTaskListView(LoginRequiredMixin, ListView):
    """ListView class only for normal tasks."""

    model = Task
    template_name = "app/normal_task_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NormalTaskListView, self).get_context_data(**kwargs)
        user = self.request.user
        normal_tasks = Task.objects.filter(priority="Normal", assignees=user).select_related()

        if self.request.GET.get("name") is not None:
            normal_tasks = normal_tasks.filter(name__icontains=self.request.GET.get("name"))

        context["normal_tasks"] = normal_tasks

        return context


class LowTaskListView(LoginRequiredMixin, generic.ListView):
    """ListView class only for low tasks."""

    model = Task
    template_name = "app/low_task_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LowTaskListView, self).get_context_data(**kwargs)
        user = self.request.user
        low_tasks = Task.objects.filter(priority="Low", assignees=user).select_related()

        if self.request.GET.get("name") is not None:
            low_tasks = low_tasks.filter(name__icontains=self.request.GET.get("name"))

        context["low_tasks"] = low_tasks

        return context


class TodayTaskListView(LoginRequiredMixin, generic.ListView):
    """ListView class only for tasks which deadline is today."""

    model = Task
    template_name = "app/today_task_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TodayTaskListView, self).get_context_data(**kwargs)
        user = self.request.user
        today_tasks = Task.objects.filter(deadline=datetime.date.today(), assignees=user).select_related()

        if self.request.GET.get("name") is not None:
            today_tasks = today_tasks.filter(name__icontains=self.request.GET.get("name"))

        context["today_tasks"] = today_tasks

        return context


class MyTaskListView(LoginRequiredMixin, generic.ListView):
    """ListView class only for tasks where executor is current login user."""

    model = Task
    template_name = "app/my_task_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MyTaskListView, self).get_context_data(**kwargs)
        user = self.request.user
        my_tasks = Task.objects.filter(assignees=user).select_related()

        if self.request.GET.get("name") is not None:
            my_tasks = my_tasks.filter(name__icontains=self.request.GET.get("name"))

        context["my_tasks"] = my_tasks

        return context


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    """CreateView class for creating tasks."""

    model = Task
    form_class = CreateTaskForm
    template_name = "app/task_form.html"
    success_url = reverse_lazy("app:index")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    """UpdateView class for updating tasks."""
    model = Task
    form_class = UpdateTaskForm
    success_url = reverse_lazy("app:index")

    def get_context_data(self, **kwargs):
        context = super(TaskUpdateView, self).get_context_data(**kwargs)

        # context["task"] = Task.objects.get(self.object)

        return context


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    """DeleteView class for delete tasks."""

    model = Task
    success_url = reverse_lazy("app:index")


class WorkerCreateView(generic.CreateView):
    """CreateView class for sign up and create new users."""

    model = Worker
    form_class = WorkerCreationForm
    template_name = "registration/sign_up.html"
    success_url = reverse_lazy("app:index")

    def get_context_data(self, **kwargs):
        context = super(WorkerCreateView, self).get_context_data(**kwargs)
        positions = Position.objects.all().select_related()

        context["positions"] = positions

        return context
