# coding=utf-8
from util import *

# calcul des opérations booléennes entre 2 listes d'intervalles ordonnees en 1D
# un intervalle est une paire (t1: un nombre, t2: un nombre)
# quand vos operations booleennes fonctionneront,
# changez t1 et t2 en deux contacts. Il y a un champ t dans le contact

#rend le t d'un contact, que le contact soit un nombre ou un Contact :
def tof( contact):
	if is_num( contact) : 
		return contact
	else:
		return contact.t


#pour supprimer les intervalles: (a1,a1) : purge1D( intervalles)

def purge1D( intervalles):
    if None == intervalles:
        #print("found none")
        return None
    #print(intervalles)
    a = (a1,a2)= hd( intervalles)
    if None == tof(a1) or None==tof(a2):
        #print("found none")
        return None    
    if tof(a1)==tof(a2) :
    	#print("a1 == a2")
    	return purge1D( cons( hd( tl( intervalles)), tl( tl(intervalles))))
    else:
    	return intervalles


#pour fusionner des intervalles contigus : [a1, a2], [a3==a2, a4] en [a1, a4]
def merge1D( intervalles):
	if None==intervalles or None==tl( intervalles) :
		return intervalles
	else:
		a = (a1,a2)= hd( intervalles)
		b = (b1,b2)= hd( tl( intervalles))
		if tof(a2)==tof(b1) :
			return merge1D( cons( (a1,b2), tl( tl( intervalles))))
		else :
			return cons( a, merge1D( tl( intervalles)))

def simplify1D( intervalles): #combine purge1D et merge1D
	return purge1D( merge1D( intervalles))

def inter( a, b):
    if None==a or None==b :
    	return None     
    else:
        ((a1,a2), qa) = (hd(a), tl(a))
        ((b1,b2), qb) = (hd(b), tl(b))         
        assert( tof( a1) <= tof( a2))
        assert( tof( b1) <= tof( b2))
        if tof( a1) > tof( b1) :
        	return inter( b, a)
        elif tof( a2) < tof( b1) :
        	return inter( qa, b)
        elif tof( b2) <= tof( a2) :
        	return cons( (b1, b2), inter( a, qb))
        else:
    	    return cons( (b1, a2), inter( qa, b))

'''
def union(a, b):
    if a is None:
        return b
    elif b is None:
        return a
    else:
        (ta, qa) = (hd(a), tl(a))
        (tb, qb) = (hd(b), tl(b))
        (a1, a2) = ta
        (b1, b2) = tb       
        assert (tof(a1) <= tof(a2))
        assert (tof(b1) <= tof(b2))
        if tof(a1) > tof(b1):
            return union(b, a)
        elif tof(a2) < tof(b1):
            return cons(ta, union(qa, b))
        elif tof(b2) <= tof(a2):
            return union(a, qb)
        else:
            return union(cons((a1, b2), qb), qa)
'''

def union( a, b):
    if None==a:
    	return b
    elif None==b:
    	return a
    else:
        ((a1,a2), qa) = (hd(a), tl(a))
        ((b1,b2), qb) = (hd(b), tl(b))
        assert( tof( a1) <= tof( a2))
        assert( tof( b1) <= tof( b2))
        if tof( a1) > tof( b1) :
        	return union(b, a)
		# ta commence avant tb :
        elif tof( a2) < tof( b1) :
			# ta finit avant que que tb, et donc b commencent :
        	return cons((a1, a2), union(qa, b))
        elif tof( b2) <= tof( a2) :
			# tb est inclus dans ta :
			#on cons une liste avec ta et tb et on passe au prochain element
        	return cons(( a1, a2), union(qa, qb))
        else: 
            return cons(( a1, b2), union(qa, qb))
			# ordre= a1, b1, a2, b2:
			#l'intervalle [b1, a2] est incluse dans l'union (cons) et on passe a l'element suivant


def oppose1D(a):
    ((a1,a2), qa) = (hd(a), tl(a))
    tmp = cons( ( tof(a1), tof(a2)), qa)
    tmp = ltov(tmp)
    #print(tmp)
    oppose = (len(tmp)+1)*[(0, 0)]
    oppose[0] = (0, tmp[0][0])
    #print('tmp1 =',tmp[0][1])
    j = 1
    for i in range(1, len(tmp)):
    	print(i)
    	#print(tmp[i-1][1],'et', tmp[i][0])
    	oppose[i] = (tmp[i-1][1], tmp[i][0])
    	#print(oppose[i])
    oppose[len(tmp)] = (tmp[len(tmp)-1][1], math.inf) 
    listeO = vtol(oppose)
    #print(listeO)
    return listeO

'''
def differ(a, b):
    if None==a or None==b :
	    return None
    return inter(a, oppose1D(b))
'''

def differ(a, b):
    if None == a:
        return None
    elif None==b:
        return None
    else:
        ((a1,a2), qa) = (hd(a), tl(a))    
        ((b1,b2), qb) = (hd(b), tl(b))
        assert( tof(a1) < tof(a2))
        assert(tof(b1) < tof(b2))
        if tof(b2) <= tof(a1):
            return differ(a, qb)
        elif tof(a2) <= tof(b1):
            return cons((a1, a2), differ(qa, b))
        elif tof(b1) <= tof(a1):
            if tof(b2) <= tof(a2):
                return differ( ((b2, a2), qa), qb)
            else:
                return differ(qa, b)
        elif tof(a2) <= tof(b2):
            return cons((a1, b1), differ(qa, b))
        else:
            return cons( (a1, b1), differ( cons( (b2, a2), qa), qb))

def inter1D( a, b):
    if None==a or None==b :
	    return None
    return simplify1D(inter( a, b))

def union1D( a, b):
    if None==a or None==b :
	    return None
    return simplify1D(union( a, b))

def differ1D( a, b) :
    if None==a or None==b :
        return None
    return simplify1D(differ(a, b))

a=vtol( [(1, 2), (4, 20), (24, 36)])
b=vtol( [(4, 7), (10, 10), (10, 22), (23, 40), (50, 100)])
print("apres simplify pm : A U B = ", union1D(a, b))


