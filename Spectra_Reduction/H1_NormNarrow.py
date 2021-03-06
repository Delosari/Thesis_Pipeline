import os
import sys
sys.path.append('/home/vital/git/Dazer/Dazer/dazer/')
os.environ['TCL_LIBRARY'] = '/home/vital/anaconda/python27/lib/tcl8.5'
os.environ['TK_LIBRARY'] = '/home/vital/anaconda/python27/lib/tk8.5'
from DZ_observation_reduction import spectra_reduction

'''
Run externally
python /home/vital/git/Thesis_Pipeline/Thesis_Pipeline/Spectra_Reduction/H1_NormNarrow.py
'''

#Load iraf pypeline object
dz = spectra_reduction()

#Load reduction data frame
dz.declare_catalogue(dz.Catalogue_folder)

#Loop through the arms--
colors = ['Red']

data_dict = {'reduc_tag' : 'norm_narrow'}

for arm_color in colors:
      
    indeces_Stars   = (dz.reducDf.reduc_tag == 'clean_narrow') & (dz.reducDf.ISIARM == '{color} arm'.format(color = arm_color)) & (dz.reducDf.valid_file)
  
    Files_Folders   = dz.reducDf.loc[indeces_Stars, 'file_location'].values
    Files_Names     = dz.reducDf.loc[indeces_Stars, 'file_name'].values
    objects         = dz.reducDf.loc[indeces_Stars, 'frame_tag'].values
    number_objects  = len(Files_Names)
     
    for i in range(number_objects):
                                             
        #Names configuration
        initial_name    = Files_Folders[i] + Files_Names[i]
        Normalize_Name  = Files_Folders[i] + objects[i] + '_clean_n.fits'
               
        #-----Clean the spectra
        dz.task_attributes['color']         = arm_color
        dz.task_attributes['run folder']    = '{folder_run}'.format(folder_run = dz.reducFolders['objects'])
        dz.task_attributes['input']         = initial_name
        dz.task_attributes['output']        = Normalize_Name
          
        #Run the task
        dz.run_iraf_task('continuum', run_externally=False)
             
        #Add objects to data frame with the new frame_tag
        dz.object_to_dataframe(Normalize_Name, data_dict)        
    
indeces_print = (dz.reducDf.reduc_tag == 'norm_narrow')
dz.generate_step_pdf(indeces_print, file_address = dz.reducFolders['reduc_data'] + 'normalized_narrow_stars', plots_type = 'spectra', ext = 0)        
                            
print 'Data treated'



