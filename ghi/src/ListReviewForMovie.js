
import React, { useState, useEffect } from "react"

import './style.css'


function ListReviewForMovie(data) {
  //declare new state variable 

  const [reviews, setReviews] = useState([])

  //fetches review data 


  useEffect(() => {
    async function getData() {

      const url = `http://localhost:8090/api/reviews/${data.imdb_id}/`

      const response = await fetch(url);

      if (response.ok) {
        const data = await response.json();
        setReviews(data)
      }

    }
    getData()

  }, [])

  const checkIfRatings = (rating) => {
    return (
      <>
        <div className="star-rating">
          {[...Array(rating)].map((star) => {
            return (
              <span className="star">&#9733;</span>
            );
          })}
        </div>

      </>
    )
  }






  return (




    <div className="mt-4">
      <div className="flex-grow-1 flex-shrink-1">
        <div className="shadow p-4 mb-5 bg-white rounded">
          <div className="p-3 mb-3 mb-md-0 mr-md-3 bg-light scroll">



            {reviews?.map((review) => {



              return (

                <div className="text"><br />

                  <h6 key={review.id}>{review.title}</h6>

                  <span className="user">@{review.user.user_name}</span>


                  <span className="style">{'\t'}{review.date}</span>




                  {checkIfRatings(review.rating)}

                  {review.post}
                  <br />

                </div>




              )
            })
            }


          </div>

        </div>


      </div>
    </div >





  )
}

export default ListReviewForMovie