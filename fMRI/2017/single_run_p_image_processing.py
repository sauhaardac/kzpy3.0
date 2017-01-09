from kzpy3.vis import *





mask = zeros((128,128))
mask[25:128-25,10:118]=1.
q = 6
mask[128/2-q:128/2+q,128/2-q:128/2+q]=0.
mask = mask[16:112,:]
mask2 = mask.copy()
mask2[19:109,2:126] = 1.
mi(mask,'mask')

thresh = 10.







mask_dic_2 = {}
mask_dic_2['vase'] = {}
mask_dic_2['face'] = {}
mask_dic_2['space'] = {}

mask_dic_2['vase'][100] = '1_vase.png'
mask_dic_2['vase'][101] = '2_vase.png'
mask_dic_2['vase'][102] = '3_vase.png'
mask_dic_2['vase'][103] = '4_vase.png'

mask_dic_2['face'][100] = '1_face.png'
mask_dic_2['face'][101] = '2_face.png'
mask_dic_2['face'][102] = '3_face.png'
mask_dic_2['face'][103] = '4_face.png'

mask_dic_2['space'][100] = '1_space.png'
mask_dic_2['space'][101] = '2_space.png'
mask_dic_2['space'][102] = '3_space.png'
mask_dic_2['space'][103] = '4_space.png'


blank = zeros((128,128))
mask_path = opjD('/Users/karlzipser/Desktop/19July2015_1Jan2016_p-imaging_results/S1_2014_S6_2015_images_and_masks/Vermeer_masks')
for t in mask_dic_2:
	for n in mask_dic_2[t]:
		#blank = 0*blank
		#blank[16:96+16] = z2o(imread(opj(mask_path,mask_dic_2[t][n]))[:,:,0])
		mask_dic_2[t][n] = z2o(imread(opj(mask_path,mask_dic_2[t][n]))[:,:,0]) #mask2 * blank


mask_dic_1 = {}
mask_dic_1['vase'] = {}
mask_dic_1['face'] = {}
mask_dic_1['space_near_vase'] = {}
mask_dic_1['space_near_face'] = {}

mask_dic_1['vase'][2] = 'Vermeer_2_mask_vase.png'
mask_dic_1['vase'][3] = 'Vermeer_3_mask_vase.png'
mask_dic_1['vase'][4] = 'Vermeer_4_mask_vase.png'
mask_dic_1['vase'][5] = 'Vermeer_5_mask_vase.png'


mask_dic_1['face'][2] = 'Vermeer_2_mask_face.png'
mask_dic_1['face'][3] = 'Vermeer_3_mask_face.png'
mask_dic_1['face'][4] = 'Vermeer_4_mask_face.png'
mask_dic_1['face'][5] = 'Vermeer_5_mask_face.png'


mask_dic_1['space_near_vase'][2] = 'Vermeer_2_mask_near_vase.png'
mask_dic_1['space_near_vase'][3] = 'Vermeer_3_mask_near_vase.png'
mask_dic_1['space_near_vase'][4] = 'Vermeer_4_mask_near_vase.png'
mask_dic_1['space_near_vase'][5] = 'Vermeer_5_mask_near_vase.png'


mask_dic_1['space_near_face'][2] = 'Vermeer_2_mask_near_face.png'
mask_dic_1['space_near_face'][3] = 'Vermeer_3_mask_near_face.png'
mask_dic_1['space_near_face'][4] = 'Vermeer_4_mask_near_face.png'
mask_dic_1['space_near_face'][5] = 'Vermeer_5_mask_near_face.png'



blank = zeros((128,128))
mask_path = opjD('19July2015_1Jan2016_p-imaging_results/S1_2015_HVO_images_and_masks/Vermeer_masks')
for t in mask_dic_1:
	for n in mask_dic_1[t]:
		blank = 0*blank
		#blank[16:96+16] = z2o(imread(opj(mask_path,mask_dic_1[t][n]))[:,:,0])
		mask_dic_1[t][n] = z2o(imread(opj(mask_path,mask_dic_1[t][n]))[:,:,0]) #mask2 * blank



region_masks = {}
region_masks['S1_2015'] = mask_dic_1
region_masks['S6_2015'] = mask_dic_2
region_masks['S1_2014'] = mask_dic_2

painting_dic = {}
painting_dic['S1_2015'] = {}
painting_dic['S1_2015'][2] = 'Vermeer_2.jpg'
painting_dic['S1_2015'][3] = 'Vermeer_3.jpg'
painting_dic['S1_2015'][4] = 'Vermeer_4.jpg'
painting_dic['S1_2015'][5] = 'Vermeer_5.jpg'
painting_path = opjD('19July2015_1Jan2016_p-imaging_results/S1_2015_HVO_images_and_masks/Vermeer_512')
for p in painting_dic['S1_2015']:
	painting_dic['S1_2015'][p] = imread(opj(painting_path,painting_dic['S1_2015'][p]))
painting_dic['S1_2014'] = {}
painting_dic['S1_2014'][100] = '1.png'
painting_dic['S1_2014'][101] = '2.png'
painting_dic['S1_2014'][102] = '3.png'
painting_dic['S1_2014'][103] = '4.png'
painting_path = opjD('19July2015_1Jan2016_p-imaging_results/S1_2014_S6_2015_images_and_masks/Vermeer_images')
for p in painting_dic['S1_2014']:
	painting_dic['S1_2014'][p] = imread(opj(painting_path,painting_dic['S1_2014'][p]))
painting_dic['S6_2015'] = painting_dic['S1_2014']

path = opjD('19July2015_1Jan2016_p-imaging_results/single_run_p_images')

subjects,_ = dir_as_dic_and_list(path)

for s in subjects:
	subjects[s] = {}
	subjects[s]['tasks_raw'],_ =  dir_as_dic_and_list(opj(path,s))
	for t in subjects[s]['tasks_raw']:
		task = t.split('.')[0]
		subjects[s][task] = {}
		subjects[s]['tasks_raw'][t] = {}
		_,subjects[s]['tasks_raw'][t] = sorted(dir_as_dic_and_list(opj(path,s,t)))
		for f in subjects[s]['tasks_raw'][t]:
			print (s,t,f)
			if len(f.split('_')) > 1:
				img_num = 100 + int(f.split('.')[0].split('_')[-1])
			else:
				img_num = int(f.split('.')[0])
				if img_num > 6:
					img_num -= 6
			if img_num not in subjects[s][task]:
				subjects[s][task][img_num] = []
			img = imread(opj(path,s,t,f))
			if shape(img)[0] == 128:
				img = img[16:112,:]

			img = 1.0 * img
			values = []
			for x in range(shape(img)[0]):
				for y in range(shape(img)[1]):
					if mask[x,y] > 0.5:
						values.append(img[x,y])
			values = array(values)
			vmean = values.mean()
			vstd = values.std()
			img -= vmean
			img /= vstd
			img[img > thresh] = thresh
			img[img < -thresh] = -thresh

			subjects[s][task][img_num].append(img)






from scipy import stats
def ttest(a,b):
	return stats.ttest_ind(a,b)[1]


def get_region_stats(subject,task,painting,region_masks,painting_dic,position):
	#plt.close('all')
	painting_img = painting_dic[subject][painting]
	mi(painting_img,d2s('Painting','painting'))
	small_painting_img = imresize(painting_img,(96,128))
	msk = region_masks[subject][position][painting]
	for i in range(3):
		small_painting_img[:,:,i] *= msk
	mi(small_painting_img,'masked painting')
	
	do_clf = False
	figure('runs')
	clf()
	mi(array(subjects[subject][task][painting]).mean(axis=0),'runs',[4,4,16])
	pause(0.0001)
	vals = []
	msk_sum = msk.sum()
	for i in range(len(subjects[subject][task][painting])):
		if i > 0:
			do_clf = False
		mi(subjects[subject][task][painting][i],'runs',[4,4,i+1],do_clf=do_clf,img_title=d2s(i))
		pause(0.0001)
		vals.append(( msk * subjects[subject][task][painting][i]).sum() / msk_sum )
	pause(0.0001)
	return array(vals)



region_stats = {}
for s in sorted(subjects):
	for t in sorted(subjects[s]):
		if t in sorted(['attend_face','attend_vase','read_letters']):
			for p in sorted(subjects[s][t]):
				if p != 1 and p != 6:
					for position in ['face','vase']:
						region_stats[(s,t,p,position)] = get_region_stats(s,t,p,region_masks,painting_dic,position)

n = 5
for s in subjects.keys():
	for p in sorted(painting_dic[s].keys()):
		vv=region_stats[s,'attend_vase',p,'vase']
		fv=region_stats[s,'attend_face',p,'vase']
		rv=region_stats[s,'read_letters',p,'vase']
		vf=region_stats[s,'attend_vase',p,'face']
		ff=region_stats[s,'attend_face',p,'face']
		rf=region_stats[s,'read_letters',p,'face']
		print(d2f('\t',s,dp(ttest(vv,fv),n),dp(ttest(vf,ff),n),dp(ttest(vv,rv),n),dp(ttest(rf,ff),n),dp(ttest(vf,rf),n),dp(ttest(rv,fv),n),p))

"""
				(vv,fv)	(vf,ff)	(vv,rv)	(rf,ff)	(vf,rf)	(rv,fv) p
		S1_2015	0.0		0.03465	0.0		0.18073	0.18349	0.4737	2
		S1_2015	0.0		0.00026	0.0		0.00043	0.74645	0.01185	3
		S1_2015	6e-05	0.0		0.0		0.01187	0.00076	0.15281	4
		S1_2015	0.0		0.00056	0.0		0.51094	0.00086	0.77597	5
		S1_2014	0.03548	0.28494	0.0238	0.1673	0.62966	0.90329	100
		S1_2014	0.05655	0.16875	1e-05	0.4734	0.35452	0.02259	101
		S1_2014	0.00336	0.03385	1e-05	0.08407	0.97614	0.00327	102
		S1_2014	0.02738	0.0431	0.00525	0.03169	0.42967	0.39049	103
		S6_2015	0.00045	0.62566	0.00138	0.86215	0.69397	0.3946	100
		S6_2015	0.00192	0.01422	0.00255	0.02276	0.60163	0.24409	101
		S6_2015	0.0467	0.00341	0.03477	0.0018	0.36701	0.97589	102
		S6_2015	0.00259	3e-05	0.00314	0.00201	0.01612	0.9834	103

Vase region, attend vase vs. read letters significant at p<0.05 or better for all subjects and all paintings.
Face region, attend face vs. read letters, significant at p<0.05 or better for 3 out of 4 paintings for Subjects 2 & 3, and for 1 out of 4 paintings for Subject 4.
"""







plt.close('all')

matplotlib.rcParams.update({'font.size': 22})
matplotlib.rcParams.update({'lines.linewidth': 5})
matplotlib.rcParams.update({'axes.linewidth': 5})
matplotlib.rcParams.update({'lines.markersize': 5})
m = 20
#figure(Subject,facecolor="white")

symbols = {}
symbols['S1_2014'] = 'o'
symbols['S6_2015'] = 'D'
symbols['S1_2015'] = 's'

def plot_with_error(a,b,s='o',m=5,fig=False,color='r'):
	if fig != False:
		figure(fig)
	plt.errorbar(a.mean(),b.mean(),xerr=a.std()/sqrt(len(a)),yerr=b.std()/sqrt(len(b)),fmt=s+color,markersize=m)
mn,mx = -1,3

plt_dic = {}
plt_dic['rf,ff'] = ['read letters','attention task','Face Region','r']
plt_dic['rv,vv'] = ['read letters','attention task','Vase Region','b']
plt_dic['rf,vf'] = ['read letters','attention task','Face Region','b']
plt_dic['rv,fv'] = ['read letters','attention task','Vase Region','r']

for fig in plt_dic:
	figure(plt_dic[fig][2],facecolor="white")
	clf()
	plot([mn,mx],[mn,mx],'k:')
	plt.axis((mn,mx,mn,mx))
	plt_square()
	plt.ylabel(plt_dic[fig][1])
	plt.xlabel(plt_dic[fig][0])
	title(plt_dic[fig][2])

for s in subjects.keys():
	for p in sorted(painting_dic[s].keys()):
		vv=region_stats[s,'attend_vase',p,'vase']
		fv=region_stats[s,'attend_face',p,'vase']
		rv=region_stats[s,'read_letters',p,'vase']
		vf=region_stats[s,'attend_vase',p,'face']
		ff=region_stats[s,'attend_face',p,'face']
		rf=region_stats[s,'read_letters',p,'face']
		for fig in plt_dic:
			exec("""plot_with_error("""+fig+""",s=symbols[s],m=m,fig='"""+plt_dic[fig][2]+"""',color='"""+plt_dic[fig][3]+"""')""")

		print(d2f('\t',s,dp(ttest(vv,fv),n),dp(ttest(vf,ff),n),dp(ttest(vv,rv),n),dp(ttest(rf,ff),n),dp(ttest(vf,rf),n),dp(ttest(rv,fv),n),p))



from matplotlib.backends.backend_pdf import PdfPages

for f in ['Face Region','Vase Region']:
	fig = figure(f)
	pp = PdfPages(opjD(f.replace(' ','-')+'.pdf'))
	pp.savefig(fig)
	pp.close()


