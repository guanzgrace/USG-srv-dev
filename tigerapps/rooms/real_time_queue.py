import time
from rooms.models import *
from gevent import spawn, sleep
from gevent.event import Event
from gevent.coros import BoundedSemaphore
import subprocess
import os, sys
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

DEFAULT_CLEAR_INTERVAL = 10*60

class LastQueueUpdate(object):
    def __init__(self, queue_id=0, update=None):
        self.event = Event()
        if update:
            self.update = update
        else:
            self.update = QueueUpdate.objects.filter(queue__id=queue_id).order_by('-id')[0]

class QueueManager(object):
    
    def __init__(self, clear_interval=DEFAULT_CLEAR_INTERVAL):
        self.__updates = {}
        self.__updates_lock = BoundedSemaphore()
        # Start clearing daemon thread.
        spawn(self._daemon_clear, interval=clear_interval)

    def _load(self, queue_id):
        """Load and return queue update tracker for queue_id."""
        self.__updates_lock.acquire()
        if queue_id in self.__updates:
            self.__updates_lock.release()
            return self.__updates[queue_id]
        try:
            self.__updates[queue_id] = LastQueueUpdate(queue_id=queue_id)
        except:
            update = QueueUpdate(queue=Queue.objects.get(id=queue_id),
                                 timestamp = int(time.time()),
                                 kind = QueueUpdate.EDIT,
                                 kind_id = 1)
            self.__updates[queue_id] = LastQueueUpdate(update=update)        
        self.__updates_lock.release()
        return self.__updates[queue_id]

    def _clear(self):
        """Clear the in-memory update tracking dictionary"""
        self.__updates_lock.acquire()
        print 'Clearing'
        # Make sure anyone currently waiting reloads.
        for queue_id in self.__updates:
            self.__updates[queue_id].event.set()
            self.__updates[queue_id].event.clear()
        self.__updates = {}
        print 'Clear'
        self.__updates_lock.release()

    def _daemon_clear(self, interval):
        """Clear the update tracking dictionary every interval seconds."""
        while True:
            sleep(interval)
            self._clear()

    def edit(self, user, queue, room_idlist, draw):
        # Perform the work
        rooms = []
        print 'edit', room_idlist
        for roomid in room_idlist:
            room = Room.objects.get(pk=roomid)
            if (not room) or not draw in room.building.draw.all():
                return {'error':'bad room/draw'}
            rooms.append(room)
        # Clear out the old list
        queue.queuetoroom_set.all().delete()
        # Put in new relationships
        for i in range(0, len(rooms)):
            qtr = QueueToRoom(queue=queue, room=rooms[i], ranking=i)
            qtr.save()
        
        update = QueueUpdate(queue=queue, timestamp=int(time.time()), 
                              kind=QueueUpdate.EDIT, kind_id=user.id)
        update.save()
        latest = self._load(queue.id)
        latest.update = update
        latest.event.set()
        latest.event.clear()
        room_list = []
        for room in rooms:
            room_list.append({'id':room.id, 'number':room.number,
                              'building':room.building.name})
        return {'rooms':room_list}

    def check(self, user, queue, last_id):
        print user, queue, last_id
        latest = self._load(queue.id)
        if last_id == latest.update.id:
            print 'going to wait'
            print latest.update.id
            latest.event.wait()
            latest = self._load(queue.id)
        print 'past wait'
        queueToRooms = QueueToRoom.objects.filter(queue=queue).order_by('ranking')
        if not queueToRooms:
            return {'id':latest.update.id, 'rooms':[]}
        room_list = []
        if latest.update.kind == QueueUpdate.EDIT:
            netid = User.objects.get(pk=latest.update.kind_id).netid
        else:
            netid = ''
        for qtr in queueToRooms:
            room_list.append({'id':qtr.room.id, 'number':qtr.room.number,
                              'building':qtr.room.building.name})
        return {'id':latest.update.id,
                'kind':QueueUpdate.UPDATE_KINDS[latest.update.kind][1],
                'netid':netid,
                'rooms':room_list}

manager = QueueManager()

def check(user, queue, last_id):
    response = manager.check(user, queue, last_id)
    while response.get('netid') == user.netid and last_id != 0:
        response = manager.check(user, queue, response['id'])
    # Add in queue invitation notification.
    response['invites'] = QueueInvite.objects.filter(receiver=user).count()
    return response

edit = manager.edit
