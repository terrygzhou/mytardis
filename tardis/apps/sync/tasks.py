from celery.task import task
from tardis.apps.sync.models import SyncedExperiment

@task(name="tardis.apps.sync.tasks.clock_tick", ignore_result=True)

def clock_tick():

    exps = SyncedExperiment.objects.all()
    pending_exps = [exp for exp in exps if not exp.is_complete()] 
    completed_exps = [exp for exp in exps if exp.is_complete()] 
    
    print "\nPending experiments:"
    for exp in pending_exps:
        print "ID: %d State:%s" % (exp.id, exp.state)

    print "\nCompleted experiments:"
    for exp in completed_exps:
        print "ID: %d State:%s" % (exp.id, exp.state)

    for exp in pending_exps:
        exp.state = exp.state.get_next_state(exp.experiment)
        exp.save()



