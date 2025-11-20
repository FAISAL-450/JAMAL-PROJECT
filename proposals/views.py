from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from .models import Proposal, ProposalDocument
from .forms import ProposalForm, DocumentForm

@login_required
def proposal_dashboard(request, proposal_id=None):
    proposal_form = ProposalForm()
    document_form = DocumentForm()
    proposal = None

    if proposal_id:
        proposal = get_object_or_404(Proposal, id=proposal_id)

    return render(request, 'proposals/proposal_dashboard.html', {
        'proposal_form': proposal_form,
        'document_form': document_form,
        'proposal': proposal
    })

@login_required
def create_proposal(request):
    if request.method == 'POST':
        form = ProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.created_by = request.user
            proposal.save()
            return redirect('proposal_dashboard', proposal_id=proposal.id)
    else:
        form = ProposalForm()
    return render(request, 'proposals/create_proposal.html', {'form': form})

@login_required
def upload_documents(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        if form.is_valid():
            for f in files:
                ProposalDocument.objects.create(proposal=proposal, file=f)
            return redirect('proposal_dashboard', proposal_id=proposal.id)
    else:
        form = DocumentForm()
    return render(request, 'proposals/upload_documents.html', {'form': form, 'proposal': proposal})

@login_required
def view_proposal(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    return render(request, 'proposals/view_proposal.html', {'proposal': proposal})

@login_required
def send_proposal_email(request, proposal_id):
    proposal = get_object_or_404(Proposal, id=proposal_id)
    documents = proposal.documents.all()
    email = EmailMessage(
        subject=f"Proposal: {proposal.title}",
        body=proposal.description,
        to=[proposal.client_email]
    )
    for doc in documents:
        email.attach_file(doc.file.path)
    email.send()
    return redirect('proposal_dashboard', proposal_id=proposal.id)
